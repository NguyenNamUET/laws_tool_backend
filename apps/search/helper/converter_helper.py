def convert_vi_field_to_es_field(law_document):
    law_document['title'] = law_document.pop('Tên VB')
    law_document['attribute'] = law_document.pop('Thuộc tính')
    law_document['history'] = law_document.pop('Lịch sử')
    law_document['schema'] = law_document.pop('Lược đồ')
    if ('Văn bản HD, QĐ chi tiết ' in law_document['schema'] and law_document['schema'][
        'Văn bản HD, QĐ chi tiết '] is not None):
        law_document['schema']['instructions_give_document'] = law_document['schema'].pop('Văn bản HD, QĐ chi tiết ')
    if ('Văn bản bị hết hiệu lực 1 phần ' in law_document['schema'] and law_document['schema'][
        'Văn bản bị hết hiệu lực 1 phần '] is not None):
        law_document['schema']['canceled_one_part_document'] = law_document['schema'].pop(
            'Văn bản bị hết hiệu lực 1 phần ')
    if ('Văn bản bị đình chỉ' in law_document['schema'] and law_document['schema']['Văn bản bị đình chỉ'] is not None):
        law_document['schema']['suspended_document'] = law_document['schema'].pop('Văn bản bị đình chỉ')
    if ('Văn bản bổ sung' in law_document['schema'] and law_document['schema']['Văn bản bổ sung'] is not None):
        law_document['schema']['extend_document'] = law_document['schema'].pop('Văn bản bổ sung')
    if ('Văn bản căn cứ' in law_document['schema'] and law_document['schema']['Văn bản căn cứ'] is not None):
        law_document['schema']['pursuant_document'] = law_document['schema'].pop('Văn bản căn cứ')
    if ('Văn bản dẫn chiếu' in law_document['schema'] and law_document['schema']['Văn bản dẫn chiếu'] is not None):
        law_document['schema']['reference_document'] = law_document['schema'].pop('Văn bản dẫn chiếu')
    if ('Văn bản hiện thời' in law_document['schema'] and law_document['schema']['Văn bản hiện thời'] is not None):
        law_document['schema']['current_document'] = law_document['schema'].pop('Văn bản hiện thời')
    if ('Văn bản hết hiệu lực' in law_document['schema'] and law_document['schema'][
        'Văn bản hết hiệu lực'] is not None):
        law_document['schema']['canceled_document'] = law_document['schema'].pop('Văn bản hết hiệu lực')
    if ('Văn bản liên quan khác' in law_document['schema'] and law_document['schema'][
        'Văn bản liên quan khác'] is not None):
        law_document['schema']['other_document_related'] = law_document['schema'].pop('Văn bản liên quan khác')
    if ('Văn bản quy định hết hiệu lực' in law_document['schema'] and law_document['schema'][
        'Văn bản quy định hết hiệu lực'] is not None):
        law_document['schema']['cancel_document'] = law_document['schema'].pop('Văn bản quy định hết hiệu lực')
    if ('Văn bản quy định hết hiệu lực 1 phần ' in law_document['schema'] and law_document['schema'][
        'Văn bản quy định hết hiệu lực 1 phần '] is not None):
        law_document['schema']['cancel_one_part_document'] = law_document['schema'].pop(
            'Văn bản quy định hết hiệu lực 1 phần ')
    if ('Văn bản sửa đổi' in law_document['schema'] and law_document['schema']['Văn bản sửa đổi'] is not None):
        law_document['schema']['amend_document'] = law_document['schema'].pop('Văn bản sửa đổi')
    if ('Văn bản đình chỉ' in law_document['schema'] and law_document['schema']['Văn bản đình chỉ'] is not None):
        law_document['schema']['suspension_document'] = law_document['schema'].pop('Văn bản đình chỉ')
    if ('Văn bản đình chỉ 1 phần' in law_document['schema'] and law_document['schema'][
        'Văn bản đình chỉ 1 phần'] is not None):
        law_document['schema']['suspension_one_part_document'] = law_document['schema'].pop('Văn bản đình chỉ 1 phần')
    if ('Văn bản được HD, QĐ chi tiết' in law_document['schema'] and law_document['schema'][
        'Văn bản được HD, QĐ chi tiết'] is not None):
        law_document['schema']['instructions_document'] = law_document['schema'].pop('Văn bản được HD, QĐ chi tiết')
    if ('Văn bản được bổ sung ' in law_document['schema'] and law_document['schema'][
        'Văn bản được bổ sung '] is not None):
        law_document['schema']['extended_document'] = law_document['schema'].pop('Văn bản được bổ sung ')
    if ('Văn bản được sửa đổi' in law_document['schema'] and law_document['schema'][
        'Văn bản được sửa đổi'] is not None):
        law_document['schema']['amended_document'] = law_document['schema'].pop('Văn bản được sửa đổi')
    if ('Văn bản bị đình chỉ 1 phần' in law_document['schema'] and law_document['schema'][
        'Văn bản bị đình chỉ 1 phần'] is not None):
        law_document['schema']['suspended_one_part_document'] = law_document['schema'].pop('Văn bản bị đình chỉ 1 phần')

    if ('Cơ quan ban hành/ Chức danh / Người ký' in law_document['attribute'] and law_document['attribute'][
        'Cơ quan ban hành/ Chức danh / Người ký'] is not None):
        law_document['attribute']['issuing_body/office/signer'] = law_document['attribute'].pop(
            'Cơ quan ban hành/ Chức danh / Người ký')
    if ('Loại văn bản' in law_document['attribute'] and law_document['attribute']['Loại văn bản'] is not None):
        law_document['attribute']['document_type'] = law_document['attribute'].pop('Loại văn bản')
    if ('Lí do hết hiệu lực' in law_document['attribute'] and law_document['attribute'][
        'Lí do hết hiệu lực'] is not None):
        law_document['attribute']['the_reason_for_this_expiration'] = law_document['attribute'].pop(
            'Lí do hết hiệu lực')
    if ('Lý do hết hiệu lực 1 phần' in law_document['attribute'] and law_document['attribute'][
        'Lý do hết hiệu lực 1 phần'] is not None):
        law_document['attribute']['the_reason_for_this_expiration_part'] = law_document['attribute'].pop(
            'Lý do hết hiệu lực 1 phần')
    if ('Lĩnh vực' in law_document['attribute'] and law_document['attribute']['Lĩnh vực'] is not None):
        law_document['attribute']['document_field'] = law_document['attribute'].pop('Lĩnh vực')
    if ('Nguồn thu thập' in law_document['attribute'] and law_document['attribute']['Nguồn thu thập'] is not None):
        law_document['attribute']['collection_source'] = law_document['attribute'].pop('Nguồn thu thập')
    if ('Ngành' in law_document['attribute'] and law_document['attribute']['Ngành'] is not None):
        law_document['attribute']['document_department'] = law_document['attribute'].pop('Ngành')
    if ('Ngày ban hành' in law_document['attribute'] and law_document['attribute']['Ngày ban hành'] is not None):
        law_document['attribute']['issued_date'] = law_document['attribute'].pop('Ngày ban hành')
    if ('Ngày có hiệu lực' in law_document['attribute'] and law_document['attribute']['Ngày có hiệu lực'] is not None):
        law_document['attribute']['effective_date'] = law_document['attribute'].pop('Ngày có hiệu lực')
    if ('Ngày hết hiệu lực' in law_document['attribute'] and law_document['attribute'][
        'Ngày hết hiệu lực'] is not None):
        law_document['attribute']['expiry_date'] = law_document['attribute'].pop('Ngày hết hiệu lực')
    if ('Ngày đăng công báo' in law_document['attribute'] and law_document['attribute'][
        'Ngày đăng công báo'] is not None):
        law_document['attribute']['gazette_date'] = law_document['attribute'].pop('Ngày đăng công báo')
    if ('Phạm vi' in law_document['attribute'] and law_document['attribute']['Phạm vi'] is not None):
        law_document['attribute']['effective_area'] = law_document['attribute'].pop('Phạm vi')
    if ('Số ký hiệu' in law_document['attribute'] and law_document['attribute']['Số ký hiệu'] is not None):
        law_document['attribute']['official_number'] = law_document['attribute'].pop('Số ký hiệu')
    if ('Thông tin' in law_document['attribute'] and law_document['attribute']['Thông tin'] is not None):
        law_document['attribute']['document_info'] = law_document['attribute'].pop('Thông tin')
    if ('Thông tin áp dụng' in law_document['attribute'] and law_document['attribute'][
        'Thông tin áp dụng'] is not None):
        law_document['attribute']['information_applicable'] = law_document['attribute'].pop('Thông tin áp dụng')

    del law_document["Toàn văn"]
    del law_document["VB Tiếng anh"]
    del law_document["VB Liên Quan"]

    return law_document