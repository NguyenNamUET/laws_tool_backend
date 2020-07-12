from datetime import datetime

def version(keep_date=False):
    present = datetime.now()
    if keep_date:
        return str(present.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        name_from_time = str(present)[:10].replace("-", "") + "_" + str(present)[11:19].replace(":", "")
        return name_from_time


VERSION = version(keep_date=True)
DATA_PATH = "/home/nguyennam/Downloads/vnu-law/crawler/thuvienphapluat.vn/20200218_171250/transform"
SCHEMA = {
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "source_id",
    "source",
    "url",
    "title",
    "html_text",
    "last_updated_time",
    "full_text",
    "attribute",
    "schema"
  ],
  "properties": {
    "source_id": {
      "$id": "#/properties/source_id",
      "type": "string"
    },
    "source": {
      "$id": "#/properties/source",
      "type": "string"
    },
    "url": {
      "$id": "#/properties/url",
      "type": "string"
    },
    "title": {
      "$id": "#/properties/title",
      "type": "string"
    },
    "html_text": {
      "$id": "#/properties/html_text",
      "type": "string"
    },
    "last_updated_time": {
      "$id": "#/properties/last_updated_time",
      "type": "string"
    },
    "full_text": {
      "$id": "#/properties/full_text",
      "type": "string"
    },
    "attribute": {
      "$id": "#/properties/attribute",
      "type": "object",
      "required": [
        "official_number",
        "document_info",
        "issuing_body/office/signer",
        "document_type",
        "document_field",
        "issued_date",
        "effective_date",
        "enforced_date",
        "the_reason_for_this_expiration",
        "the_reason_for_this_expiration_part",
        "effective_area",
        "expiry_date",
        "gazette_date",
        "information_applicable",
        "document_department",
        "collection_source"
      ],
      "properties": {
        "official_number": {
          "$id": "#/properties/attribute/properties/official_number",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/official_number/items",
            "type": "string"
          }
        },
        "document_info": {
          "$id": "#/properties/attribute/properties/document_info",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/document_info/items",
            "type": "string"
          }
        },
        "issuing_body/office/signer": {
          "$id": "#/properties/attribute/properties/issuing_body/office/signer",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/issuing_body/office/signer/items",
            "type": "string"
          }
        },
        "document_type": {
          "$id": "#/properties/attribute/properties/document_type",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/document_type/items",
            "type": "string"
          }
        },
        "document_field": {
          "$id": "#/properties/attribute/properties/document_field",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/document_field/items",
            "type": "string"
          }
        },
        "issued_date": {
          "$id": "#/properties/attribute/properties/issued_date",
          "type": "string",
          "pattern": "^(.*)$"
        },
        "effective_date": {
          "$id": "#/properties/attribute/properties/effective_date",
          "type": "string"
        },
        "enforced_date": {
          "$id": "#/properties/attribute/properties/enforced_date",
          "type": "string"
        },
        "the_reason_for_this_expiration": {
          "$id": "#/properties/attribute/properties/the_reason_for_this_expiration",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/the_reason_for_this_expiration/items",
            "type": "string"
          }
        },
        "the_reason_for_this_expiration_part": {
          "$id": "#/properties/attribute/properties/the_reason_for_this_expiration_part",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/the_reason_for_this_expiration_part/items",
            "type": "string"
          }
        },
        "effective_area": {
          "$id": "#/properties/attribute/properties/effective_area",
          "type": "string"
        },
        "expiry_date": {
          "$id": "#/properties/attribute/properties/expiry_date",
          "type": "string"
        },
        "gazette_date": {
          "$id": "#/properties/attribute/properties/gazette_date",
          "type": "string"
        },
        "information_applicable": {
          "$id": "#/properties/attribute/properties/information_applicable",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/information_applicable/items",
            "type": "string"
          }
        },
        "document_department": {
          "$id": "#/properties/attribute/properties/document_department",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/document_department/items",
            "type": "string"
          }
        },
        "collection_source": {
          "$id": "#/properties/attribute/properties/collection_source",
          "type": "array",
          "items": {
            "$id": "#/properties/attribute/properties/collection_source/items",
            "type": "string"
          }
        }
      }
    },
    "schema": {
      "$id": "#/properties/schema",
      "type": "object",
      "required": [
        "instructions_documents",
        "current_documents",
        "instructions_give_documents",
        "canceled_documents",
        "cancel_documents",
        "pursuant_documents",
        "suspended_documents",
        "suspension_documents",
        "reference_documents",
        "other_documents_related",
        "canceled_one_part_documents",
        "cancel_one_part_documents",
        "amended_documents",
        "amend_documents",
        "extended_documents",
        "extend_documents",
        "suspended_one_part_documents",
        "suspension_one_part_documents"
      ],
      "properties": {
        "instructions_documents": {
          "$id": "#/properties/schema/properties/instructions_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/instructions_documents/items",
            "type": "string"
          }
        },
        "current_documents": {
          "$id": "#/properties/schema/properties/current_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/current_documents/items",
            "type": "string"
          }
        },
        "instructions_give_documents": {
          "$id": "#/properties/schema/properties/instructions_give_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/instructions_give_documents/items",
            "type": "string"
          }
        },
        "canceled_documents": {
          "$id": "#/properties/schema/properties/canceled_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/canceled_documents/items",
            "type": "string"
          }
        },
        "cancel_documents": {
          "$id": "#/properties/schema/properties/cancel_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/cancel_documents/items",
            "type": "string"
          }
        },
        "pursuant_documents": {
          "$id": "#/properties/schema/properties/pursuant_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/pursuant_documents/items",
            "type": "string"
          }
        },
        "suspended_documents": {
          "$id": "#/properties/schema/properties/suspended_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/suspended_documents/items",
            "type": "string"
          }
        },
        "suspension_documents": {
          "$id": "#/properties/schema/properties/suspension_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/suspension_documents/items",
            "type": "string"
          }
        },
        "reference_documents": {
          "$id": "#/properties/schema/properties/reference_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/reference_documents/items",
            "type": "string"
          }
        },
        "other_documents_related": {
          "$id": "#/properties/schema/properties/other_documents_related",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/other_documents_related/items",
            "type": "string"
          }
        },
        "canceled_one_part_documents": {
          "$id": "#/properties/schema/properties/canceled_one_part_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/canceled_one_part_documents/items",
            "type": "string"
          }
        },
        "cancel_one_part_documents": {
          "$id": "#/properties/schema/properties/cancel_one_part_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/cancel_one_part_documents/items",
            "type": "string"
          }
        },
        "amended_documents": {
          "$id": "#/properties/schema/properties/amended_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/amended_documents/items",
            "type": "string"
          }
        },
        "amend_documents": {
          "$id": "#/properties/schema/properties/amend_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/amend_documents/items",
            "type": "string"
          }
        },
        "extended_documents": {
          "$id": "#/properties/schema/properties/extended_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/extended_documents/items",
            "type": "string"
          }
        },
        "extend_documents": {
          "$id": "#/properties/schema/properties/extend_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/extend_documents/items",
            "type": "string"
          }
        },
        "suspended_one_part_documents": {
          "$id": "#/properties/schema/properties/suspended_one_part_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/suspended_one_part_documents/items",
            "type": "string"
          }
        },
        "suspension_one_part_documents": {
          "$id": "#/properties/schema/properties/suspension_one_part_documents",
          "type": "array",
          "items": {
            "$id": "#/properties/schema/properties/suspension_one_part_documents/items",
            "type": "string"
          }
        }
      }
    }
  }
}
