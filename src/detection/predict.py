def predict(model, images):
    classes = []
    bboxes = []
    idx = []
    results = model.predict(images)
    for i, r in enumerate(results):
        bb = r.boxes
        xyxyn = list(bb.xyxyn.detach().numpy())
        bb_class = list(bb.cls)
        _idx = [i] * bb.cls.shape[0]
        
        classes.extend(bb_class)
        bboxes.extend(xyxyn)
        idx.extend(_idx)

    return {
        'id': idx, 'bbox': bboxes, 'class_predict': bb_class
    }
