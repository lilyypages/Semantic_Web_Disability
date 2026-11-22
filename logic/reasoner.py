"""Reasoning engine pakai owlready2 + HermiT."""

import os
import uuid
from pathlib import Path
from owlready2 import get_ontology, sync_reasoner_hermit, Thing, Not

ONTOLOGY_PATH = Path(__file__).parent.parent / "ontology" / "ABK_Ontology.owl"

_onto = None
_loading = False


def load_ontology():
    global _onto, _loading
    if _onto is not None:
        return _onto
    if _loading:
        raise RuntimeError("Ontology sedang dimuat, coba lagi.")
    _loading = True
    try:
        _onto = get_ontology(f"file://{ONTOLOGY_PATH}").load()
        return _onto
    finally:
        _loading = False


def get_ontology_instance():
    return load_ontology()


def analyze_case(sign_codes, age_months, duration_months, settings_count):
    """
    Bikin ChildCase sementara, jalankan reasoning, kembalikan hasil.

    Returns:
        dict: {
            "inferred_classes": [...],       # Suspected*, RedFlagCase, MultiSignCase, dll
            "related_conditions": [...],     # kondisi via hasCoreSign/hasSupportingSign
            "recommended_assessments": [...],
            "recommended_professionals": [...],
            "recommended_therapies": [...],
            "matched_signs": [...],          # evidence
        }
    """
    onto = load_ontology()
    case_id = f"Case_{uuid.uuid4().hex[:8]}"

    with onto:
        # Bikin individual sementara di class ChildCase
        CaseClass = onto.ChildCase
        case = CaseClass(case_id, namespace=onto)
        case.patientAgeMonths = [int(age_months)]
        case.symptomDurationMonths = [int(duration_months)]
        case.observedSettingsCount = [int(settings_count)]

        # Set hasObservedSign
        observed_signs = []
        for code in sign_codes:
            sign = onto.search_one(iri=f"*Sign_{code}")
            if sign:
                case.hasObservedSign.append(sign)
                observed_signs.append(sign)

    # Jalankan reasoner
    with onto:
        try:
            sync_reasoner_hermit([onto], infer_property_values=True, debug=0)
        except Exception as e:
            # Kalau Java tidak ada, tetap lanjut dengan query manual
            print(f"[reasoner] HermiT gagal: {e}. Pakai query manual.")

    # Ambil hasil: class yang di-infer
    inferred = []
    for cls in case.is_a:
        if isinstance(cls, Thing.__class__) or hasattr(cls, "iri"):
            name = getattr(cls, "name", str(cls))
            if name not in ("ChildCase", "Thing"):
                inferred.append(name)

    # Manual fallback: cek kondisi mana yang match sign
    related_conditions = []
    for cond in onto.DisabilityCondition.descendants():
        if not hasattr(cond, "hasCoreSign"):
            continue
        try:
            core = set(cond.hasCoreSign)
            if not core:
                continue
            matched = core & set(observed_signs)
            if matched:
                related_conditions.append({
                    "condition": cond.name,
                    "label": _get_label(cond),
                    "matched_core": [s.signCode[0] if s.signCode else s.name for s in matched],
                    "total_core": len(core),
                    "ratio": len(matched) / len(core),
                })
        except Exception:
            continue

    related_conditions.sort(key=lambda x: x["ratio"], reverse=True)

    # Rekomendasi dari class yang di-infer
    assessments, professionals, therapies = set(), set(), set()
    for cond_name in inferred:
        cond_cls = getattr(onto, cond_name, None)
        if cond_cls is None:
            continue
        for obj in getattr(cond_cls, "recommendsAssessment", []):
            assessments.add(_get_label(obj))
        for obj in getattr(cond_cls, "recommendsProfessional", []):
            professionals.add(_get_label(obj))
        for obj in getattr(cond_cls, "recommendsTherapy", []):
            therapies.add(_get_label(obj))

    # Hapus individual sementara
    with onto:
        onto.destroy_entity(case)

    return {
        "inferred_classes": inferred,
        "related_conditions": related_conditions[:10],
        "recommended_assessments": sorted(assessments),
        "recommended_professionals": sorted(professionals),
        "recommended_therapies": sorted(therapies),
        "matched_signs": [s.signCode[0] if s.signCode else s.name for s in observed_signs],
    }


def _get_label(entity):
    """Ambil label yang enak dibaca."""
    labels = getattr(entity, "label", None) or []
    if labels:
        return str(labels[0])
    return getattr(entity, "name", str(entity))