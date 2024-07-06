import pandas as pd

def predict(model, images):
    classes = []
    bboxes = []
    idx = []
    results = model.predict(images)
    for i, r in enumerate(results):
        bb = r.boxes
        xyxyn = list(bb.xyxyn.detach().numpy())
        cls = list(bb.cls)
        _idx = [i] * bb.cls.shape[0]
        
        classes.extend(cls)
        bboxes.extend(xyxyn)
        idx.extend(_idx)

    return pd.DataFrame.from_dict({
        'id': idx, 'bbox': bboxes, 'class_predict': cls
    })