import { Annotation, Sample } from '../../src/api/texoo-datamodel'

const text = "Preclinical fibrinolysis in patients with ST-segment elevation myocardial infarction in a rural region In the current guidelines for the treatment of patients with ST-segment elevation myocardial infarction (STEMI), the European Society of Cardiology (ESC) recommends preclinical fibrinolysis as a reperfusion therapy if, due to long transportation times, no cardiac catheterisation is available within 90-120 min."
const annotations = [ 
	new Annotation(12, null, null, "fibrinolysis", 12, "NamedEntityAnnotation", "DELETED", "GOLD", 1, false, "C0016017", null),
	new Annotation(42, null, null, "ST-segment elevation myocardial infarction", 42, "NamedEntityAnnotation", "DELETED", "GOLD", 1, false, "C1536220", null),
	new Annotation(18, null, null, "current guidelines", 110, "NamedEntityAnnotation", "DELETED", "GOLD", 1, false, "C4291682", null),
	new Annotation(9, null, null, "treatment", 137, "NamedEntityAnnotation", "DELETED", "GOLD", 1, false, "C0087111", null),	
	new Annotation(5, null, null, "STEMI", 208, "NamedEntityAnnotation", "DELETED", "GOLD", 1, false, "C1536220", null),
]

export const sample = new Sample(text.length, null, undefined, text, 0, "Sample", null, null, "Document", annotations, "en", null, null, null, false, "", null)

export const elasticResults = [
	{'cui': 'C123', 'names': ['test1'], 'semantic_type': 'test'},
	{'cui': 'C456', 'names': ['test2'], 'semantic_type': 'test'}
]
