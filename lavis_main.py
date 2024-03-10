from lavis.models import model_zoo, load_model_and_preprocess
import torch
from PIL import Image


if __name__ == '__main__':
    #print(model_zoo)
    device = 'cpu'
    timing_diagram = Image.open("timing_diagrams/and_gate.png").convert("RGB")
    centralpark = Image.open("centralpark.jpg").convert("RGB")
    #raw_image.show()

    model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True,
                                                         device=device)
    image = vis_processors["eval"](timing_diagram).unsqueeze(0).to(device)
    pred = model.generate({"image": image})
    print("Timing Diagram Caption: " + pred[0])

    image = vis_processors["eval"](centralpark).unsqueeze(0).to(device)
    pred = model.generate({"image": image})
    print("Central Park Caption: " + pred[0])

    model, vis_processors, txt_processers = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True,
                                                                      device=device)
    question = "What logical gate does the timing diagram represent? "
    image = vis_processors["eval"](timing_diagram).unsqueeze(0).to(device)
    question = txt_processers["eval"](question)
    answer = model.predict_answers(samples={"image": image, "text_input": question}, inference_method="generate")
    print(question + ": " + answer[0])

    question = "List all things you see in the image"
    image = vis_processors["eval"](centralpark).unsqueeze(0).to(device)
    question = txt_processers["eval"](question)
    answer = model.predict_answers(samples={"image": image, "text_input": question}, inference_method="generate")
    print(question + ": " + answer[0])

