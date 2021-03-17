from fastapi import APIRouter, Form, Response
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from news_cat.web.inference import clean_and_tokenize, get_model_loader
from news_cat.web.schemas import ClassificationResponse

router = APIRouter()


@router.get("/hello", tags=["test"])
async def hello_there():
    return {"msg": "Hello there"}


@router.get("/hello/{name}", tags=["test"])
async def hello_user(name: str):
    return {"msg": f"Hello {name}"}


@router.get("/ml")
async def list_models():
    models = list(get_model_loader().models.keys())
    return {"total": len(models), "models": models}


@router.post("/ml", response_model=ClassificationResponse)
async def predict(
    resp: Response, key: str = Form(...), news_txt: str = Form(...)
) -> ClassificationResponse:
    clf = get_model_loader().models.get(key)
    response = ClassificationResponse()

    if clf is None:
        resp.status_code = HTTP_400_BAD_REQUEST
        response.msg = f"`{key}` model is not available"
        return response

    all_puncts, news_toks = clean_and_tokenize(news_txt)

    if len(news_toks) == 0:
        resp.status_code = HTTP_400_BAD_REQUEST
        response.msg = "`news_txt` has zero workable tokens"
        return response

    if all_puncts:
        resp.status_code = HTTP_400_BAD_REQUEST
        response.msg = "`news_txt` full of punctuations is not allowed"
        return response

    # Pass the list of tokens to get the predicted class index
    predicted_class_idx = clf(news_toks)
    classes = get_model_loader().classes

    if predicted_class_idx < 0 or predicted_class_idx >= len(classes):
        resp.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        response.msg = "our model is going haywire..."

        return response

    response.success = True
    response.predicted_class = get_model_loader().classes[predicted_class_idx].strip()

    return response
