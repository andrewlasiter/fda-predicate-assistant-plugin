# openFDA Device API Data Dictionary

> Source: FDA openFDA Data Dictionary (Device.xlsx)
> Total fields: 354
> Endpoints: 5
> Generated: 2026-02-07

This reference contains every searchable and response field across all 9 openFDA Device API endpoints.

## 1. device/event (MAUDE Adverse Events)

**317 fields**

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | Action taken as part of the recall. |
| `additional_info_contact` | string | Contact information of the party that can be used to request additional information about the recall. |
| `adverse_event_flag` | string | Whether the report is about an incident where the use of the device is suspected to have resulted in an adverse outco... |
| `antibody_agree` | string | Agreement between all antibody results and antibody_truth. Any positive makes the result positive. All results must b... |
| `antibody_truth` | string | The true qualitative antibody presence result. |
| `ao_statement` | string | Approval order statement: a brief description of the reason for the supplement/application approval by FDA. |
| `brand_name` | string | The Proprietary/Trade/Brand name of the medical device as used in device labeling or in the catalog. This information... |
| `catalog_number` | string | The catalog, reference, or product number found on the device label or accompanying packaging to identify a particula... |
| `center_classification_date` | string |  |
| `cfres_id` | string | cfRes internal recall identifier |
| `classification` | string | Numerical designation (I, II, or III) that is assigned by FDA to a particular product recall that indicates the relat... |
| `clearance_type` | string | Denotes the submission method utilized for the submission of the 510(k). |
| `commercial_distribution_end_date` | date | Indicates the date the device is no longer held or offered for sale. See 21 CFR 807.3(b) for exceptions. The device m... |
| `commercial_distribution_status` | string | Indicates whether the device is in commercial distribution as defined under 21 CFR 807.3(b). |
| `company_name` | string | Company name associated with the labeler DUNS Number entered in the DI Record. |
| `contact` | string | Per 21 CFR 807.3(e), this is the official correspondent designated by the owner or operator of an establishment as re... |
| `control` | string | The result of the control line on the test. |
| `country_code` | string | The numeric 2 character code (ISO 3166-1 alpha-2) that designates the country of a postal delivery location (also kno... |
| `customer_contacts.email` | string | Email for the Customer contact; to be used by patients and consumers for device-related questions. |
| `customer_contacts.phone` | string | Phone number for the customer contact; to be used by patients and consumers for device-related questions. |
| `date_facility_aware` | string | Date the user facility’s medical personnel or the importer (distributor) became aware that the device has or may have... |
| `date_manufacturer_received` | string | Date when the applicant, manufacturer, corporate affiliate, etc. receives information that an adverse event or medica... |
| `date_of_event` | string | Actual or best estimate of the date of first onset of the adverse event. This field was added in 2006. |
| `date_performed` | date | This is the date the test was performed. |
| `date_report` | string | Date the initial reporter (whoever initially provided information to the user facility, manufacturer, or importer) pr... |
| `date_report_to_fda` | string | Date the user facility/importer (distributor) sent the report to the FDA, if applicable. |
| `date_report_to_manufacturer` | string | Date the user facility/importer (distributor) sent the report to the manufacturer, if applicable. |
| `days_from_symptom` | string | Days from symptom onset to blood collection. |
| `decision_description` | string | This is the full spelling associated with the abbreviated decision code (e.g. Substantially Equivalent - Postmarket S... |
| `definition` | string | Compositional definition of a medical device, based on the input of nomenclature experts, incorporating the definitio... |
| `device` | string | This is the proprietary name, or trade name, of the cleared device. |
| `device.brand_name` | string | The trade or proprietary name of the suspect medical device as used in product labeling or in the catalog (e.g. Flo-E... |
| `device.catalog_number` | string | The exact number as it appears in the manufacturer’s catalog, device labeling, or accompanying packaging. |
| `device.date_received` | string | Documentation forthcoming. TK |
| `device.date_removed_flag` | string | Whether an implanted device was removed from the patient, and if so, what kind of date was provided. |
| `device.date_returned_to_manufacturer` | string | Date the device was returned to the manufacturer, if applicable. |
| `device.device_age_text` | string | Age of the device or a best estimate, often including the unit of time used. Contents vary widely, but common pattern... |
| `device.device_availability` | string | Whether the device is available for evaluation by the manufacturer, or whether the device was returned to the manufac... |
| `device.device_evaluated_by_manufacturer` | string | Whether the suspect device was evaluated by the manufacturer. |
| `device.device_event_key` | string | Documentation forthcoming. |
| `device.device_operator` | string | The person using the medical device at the time of the adverse event. This may be a health professional, a lay person... |
| `device.device_report_product_code` | string | Three-letter FDA Product Classification Code. Medical devices are classified under <a href='http://www.fda.gov/medica... |
| `device.device_sequence_number` | string | Number identifying this particular device. For example, the first device object will have the value 1. This is an enu... |
| `device.expiration_date_of_device` | string | If available; this date is often be found on the device itself or printed on the accompanying packaging. |
| `device.generic_name` | string | The generic or common name of the suspect medical device or a generally descriptive name (e.g. urological catheter, h... |
| `device.implant_flag` | string | Whether a device was implanted or not. May be either marked N or left empty if this was not applicable. |
| `device.lot_number` | string | If available, the lot number found on the label or packaging material. |
| `device.manufacturer_d_address_1` | string | Device manufacturer address line 1. |
| `device.manufacturer_d_address_2` | string | Device manufacturer address line 2. |
| `device.manufacturer_d_city` | string | Device manufacturer city. |
| `device.manufacturer_d_country` | string | Device manufacturer country. |
| `device.manufacturer_d_name` | string | Device manufacturer name. |
| `device.manufacturer_d_postal_code` | string | Device manufacturer postal code. |
| `device.manufacturer_d_state` | string | Device manufacturer state code. |
| `device.manufacturer_d_zip_code` | string | Device manufacturer zip code. |
| `device.manufacturer_d_zip_code_ext` | string | Device manufacturer zip code extension. |
| `device.model_number` | string | The exact model number found on the device label or accompanying packaging. |
| `device.openfda` | object |  |
| `device.other_id_number` | string | Any other identifier that might be used to identify the device. Expect wide variability in the use of this field. It ... |
| `device_class` | string | A risk based classification system for all medical devices ((Federal Food, Drug, and Cosmetic Act, section 513). |
| `device_count_in_base_package` | integer | Number of medical devices in the base package. |
| `device_date_of_manufacturer` | string | Date of manufacture of the suspect medical device. |
| `device_description` | string | Additional relevant information about the device that is not already captured as a distinct GUDID data attribute. |
| `device_sizes.text` | string | Additional undefined device size not represented in the GUDID Size Type LOV. |
| `device_sizes.type` | string | Dimension type for the clinically relevant measurement of the medical device. |
| `device_sizes.unit` | string | The unit of measure associated with each clinically relevant size. |
| `device_sizes.value` | string | Numeric value for the clinically relevant size measurement of the medical device. |
| `distributor_address_1` | string | User facility or importer (distributor) address line 1. |
| `distributor_address_2` | string | User facility or importer (distributor) address line 2. |
| `distributor_city` | string | User facility or importer (distributor) city. |
| `distributor_name` | string | User facility or importer (distributor) name. |
| `distributor_state` | string | User facility or importer (distributor) two-digit state code. |
| `distributor_zip_code` | string | User facility or importer (distributor) 5-digit zip code. |
| `distributor_zip_code_ext` | string | User facility or importer (distributor) 4-digit zip code extension (zip+4 code). |
| `docket_number` | string | The assigned posted docket number in the Federal Register. |
| `establishment_type` | array of strings | Facility operation or activity, e.g. “Manufacturer” (short version). |
| `evaluation_id` | string | The unique identifier for each evaluation. |
| `event_date_created` | string | Date on which the recall record was created in the FDA database. |
| `event_date_initiated` | string | Date that the firm first began notifying the public or their consignees of the recall. |
| `event_date_posted` | string | Indicates the date FDA classified the recall, but it does not necessarily mean that the recall is new. |
| `event_date_terminated` | string | Date that FDA determined recall actions were completed and terminated the recall. For details about termination of a ... |
| `event_id` | string | A numerical designation assigned by FDA to a specific recall event used for tracking purposes. |
| `event_key` | string | Documentation forthcoming. |
| `event_location` | string | Where the event occurred. |
| `event_type` | string | Outcomes associated with the adverse event. |
| `expiration_date_of_device` | string | If available; this date is often be found on the device itself or printed on the accompanying packaging. |
| `fed_reg_notice_date` | string | Documentation forthcoming. |
| `firm_fei_number` | string | Facility identifier assigned to facility by the FDA Office of Regulatory Affairs. |
| `generic_name` | string | Common or generic name as specified in the submission. Not to be confused with the official device nomenclature name ... |
| `gmdn_terms.code` | string | GMDN Preferred Term Code of the common device type associated with the FDA PT Code. |
| `gmdn_terms.code_status` | boolean | GMDN Term Status, Active or Obsolete. |
| `gmdn_terms.definition` | string | Definition of the common device type associated with the GMDN Preferred Term Code/FDA PT Code. |
| `gmdn_terms.implantable` | boolean | GMDN Implantable flag. |
| `gmdn_terms.name` | string | Name of the common device type associated with the GMDN Preferred Term Code/FDA PT Code. |
| `gmp_exempt_flag` | string | An indication the device is exempt from Good Manufacturing Processes CFR 820. U.S. zip code of the Applicant. See [he... |
| `group` | string | Describes the portion of the panel the sample was from. E.g. "Positives," "Negatives," "HIV+", "Respiratory panel," etc. |
| `has_donation_id_number` | boolean | The Donation Identification Number is applicable to devices that are also regulated as HCT/Ps and is a number that is... |
| `has_expiration_date` | boolean | The date by which the label of a device states the device must or should be used. This date is required to be part of... |
| `has_lot_or_batch_number` | boolean | The number assigned to one or more device(s) that consist of a single type, model, class, size, composition, or softw... |
| `has_manufacturing_date` | boolean | The date on which a device is manufactured.This date is required to be part of the UDI when included on the label in ... |
| `has_serial_number` | boolean | The number that allows for the identification of a device, indicating its position within a series. This number is re... |
| `health_professional` | string | Whether the initial reporter was a health professional (e.g. physician, pharmacist, nurse, etc.) or not. |
| `identifiers.id` | string | An identifier that is the main (primary) lookup for a medical device and meets the requirements to uniquely identify ... |
| `identifiers.issuing_agency` | string | Organization accredited by FDA to operate a system for the issuance of UDIs |
| `identifiers.package_discontinue_date` | date | Indicates the date this particular package configuration is discontinued by the Labeler or removed from the marketplace. |
| `identifiers.package_status` | string | Indicates whether the package is in commercial distribution as defined under 21 CFR 807.3(b). |
| `identifiers.package_type` | string | The type of packaging used for the device. |
| `identifiers.quantity_per_package` | integer | The number of packages with the same Primary DI or Package DI within a given packaging configuration. |
| `identifiers.type` | string | Indicates whether the identifier is the Primary, Secondary, Direct Marking, Unit of Use, Package, or Previous DI |
| `identifiers.unit_of_use_id` | string | An identifier assigned to an individual medical device when a UDI is not labeled on the individual device at the leve... |
| `iga_agree` | string | Agreement between iga_result and antibody_truth. |
| `iga_result` | string | The test result for qualitative detection of IgA antibodies. |
| `igg_agree` | string | Agreement between igg_result and igg_truth. |
| `igg_result` | string | The test result for qualitative detection of IgG antibodies. |
| `igg_titer` | integer | The CDC spike titer for IgG in the sample. |
| `igg_truth` | string | The true qualitative IgG result. |
| `igm_agree` | string | Agreement between igm_result and igm_truth. |
| `igm_iga_agree` | string | Agreement between igm_iga_result and antibody_truth. |
| `igm_iga_result` | string | The test result for qualitative detection of (IgM / IgA) combined antibodies. |
| `igm_igg_agree` | string | Agreement between igm_igg_result and antibody_truth. |
| `igm_igg_result` | string | The test result for qualitative detection of (IgM / IgG) combined antibodies. |
| `igm_result` | string | The test result for qualitative detection of IgM antibodies. |
| `igm_titer` | integer | The CDC spike titer for IgM in the sample. |
| `igm_truth` | string | The true qualitative IgM result. |
| `implant_flag` | string | An indicator that the device is placed into a surgically or naturally formed cavity of the human body. Intended to re... |
| `initial_firm_notification` | string | The method(s) by which the firm initially notified the public or their consignees of a recall. A consignee is a perso... |
| `initial_report_to_fda` | string | Whether the initial reporter also notified or submitted a copy of this report to FDA. |
| `is_combination_product` | boolean | Indicates that the product is comprised of two or more regulated products that are physically, chemically, or otherwi... |
| `is_direct_marking_exempt` | boolean | The device is exempt from Direct Marking requirements under 21 CFR 801.45. |
| `is_hct_p` | boolean | Indicates that the product contains or consists of human cells or tissues that are intended for implantation, transpl... |
| `is_kit` | boolean | Indicates that the device is a convenience, combination, in vitro  diagnostic (IVD), or medical procedure kit. Kits a... |
| `is_labeled_as_no_nrl` | boolean | Indicates that natural rubber latex was not used as materials in the manufacture of the medical product and container... |
| `is_labeled_as_nrl` | boolean | Indicates that the device or packaging contains natural rubber that contacts humans as described under 21 CFR 801.437... |
| `is_otc` | boolean | Indicates that the device does not require a prescription to use and can be purchased over the counter. |
| `is_pm_exempt` | boolean | Indicates whether the device is exempt from premarket notification requirements. |
| `is_rx` | boolean | Indicates whether the device requires a prescription. |
| `is_single_use` | boolean | Indicates that the device is intended for one use or on a single patient during a single procedure. |
| `k_numbers` | array of strings | FDA-assigned premarket notification number, including leading letters. Leading letters “BK” indicates 510(k) clearanc... |
| `labeler_duns_number` | string | The DUNS Number is a unique nine-digit identifier for businesses. It is used to establish a D&B® business credit file... |
| `life_sustain_support_flag` | string | An indicator that the device is essential to, or yields information that is essential to, the restoration or continua... |
| `lot_number` | string | The manufacturer's unique identification of the lot(s) from which the tested devices were drawn. |
| `manufacturer` | string | Name of manufacturer or company that makes this product. |
| `manufacturer_address_1` | string | Suspect medical device manufacturer address line 1. |
| `manufacturer_address_2` | string | Suspect medical device manufacturer address line 2. |
| `manufacturer_city` | string | Suspect medical device manufacturer city. |
| `manufacturer_contact_address_1` | string | Suspect medical device manufacturer contact address line 1. |
| `manufacturer_contact_address_2` | string | Suspect medical device manufacturer contact address line 2. |
| `manufacturer_contact_area_code` | string | Manufacturer contact person phone number area code. |
| `manufacturer_contact_city` | string | Manufacturer contact person city. |
| `manufacturer_contact_country` | string | Manufacturer contact person two-letter country code. Note: For medical device adverse event reports, comparing countr... |
| `manufacturer_contact_exchange` | string | Manufacturer contact person phone number exchange. |
| `manufacturer_contact_extension` | string | Manufacturer contact person phone number extension. |
| `manufacturer_contact_f_name` | string | Manufacturer contact person first name. |
| `manufacturer_contact_l_name` | string | Manufacturer contact person last name. |
| `manufacturer_contact_pcity` | string | Manufacturer contact person phone number city code. |
| `manufacturer_contact_pcountry` | string | Manufacturer contact person phone number country code. Note: For medical device adverse event reports, comparing coun... |
| `manufacturer_contact_phone_number` | string | Manufacturer contact person phone number. |
| `manufacturer_contact_plocal` | string | Manufacturer contact person local phone number. |
| `manufacturer_contact_postal_code` | string | Manufacturer contact person postal code. |
| `manufacturer_contact_state` | string | Manufacturer contact person two-letter state code. |
| `manufacturer_contact_t_name` | string | Manufacturer contact person title (Mr., Mrs., Ms., Dr., etc.) |
| `manufacturer_contact_zip_code` | string | Manufacturer contact person 5-digit zip code. |
| `manufacturer_contact_zip_ext` | string | Manufacturer contact person 4-digit zip code extension (zip+4 code). |
| `manufacturer_country` | string | Suspect medical device manufacturer two-letter country code. Note: For medical device adverse event reports, comparin... |
| `manufacturer_g1_address_1` | string | Device manufacturer address line 1. |
| `manufacturer_g1_address_2` | string | Device manufacturer address line 2. |
| `manufacturer_g1_city` | string | Device manufacturer address city. |
| `manufacturer_g1_country` | string | Device manufacturer two-letter country code. Note: For medical device adverse event reports, comparing country codes ... |
| `manufacturer_g1_name` | string | Device manufacturer name. |
| `manufacturer_g1_postal_code` | string | Device manufacturer address postal code. |
| `manufacturer_g1_state` | string | Device manufacturer address state. |
| `manufacturer_g1_zip_code` | string | Device manufacturer address zip code. |
| `manufacturer_g1_zip_code_ext` | string | Device manufacturer address zip code extension. |
| `manufacturer_link_flag` | string | Indicates whether a user facility/importer-submitted (distributor-submitted) report has had subsequent manufacturer-s... |
| `manufacturer_name` | string | Suspect medical device manufacturer name. |
| `manufacturer_postal_code` | string | Suspect medical device manufacturer postal code. May contain the zip code for addresses in the United States. |
| `manufacturer_state` | string | Suspect medical device manufacturer two-letter state code. |
| `manufacturer_zip_code` | string | Suspect medical device manufacturer 5-digit zip code. |
| `manufacturer_zip_code_ext` | string | Suspect medical device manufacturer 4-digit zip code extension (zip+4 code). |
| `mdr_report_key` | string | A unique identifier for a report. |
| `mdr_text.date_report` | string | Date the initial reporter (whoever initially provided information to the user facility, manufacturer, or importer) pr... |
| `mdr_text.mdr_text_key` | string | Documentation forthcoming. |
| `mdr_text.patient_sequence_number` | string | Number identifying this particular patient. For example, the first patient object will have the value 1. This is an e... |
| `mdr_text.text` | string | Narrative text or problem description. |
| `mdr_text.text_type_code` | string | String that describes the type of narrative contained within the text field. |
| `medical_specialty` | string | Regulation Medical Specialty is assigned based on the regulation (e.g. 21 CFR Part 888 is Orthopedic Devices) which i... |
| `medical_specialty_description` | string | Same as above but with the codes replaced with a human readable description. Note that & and and have been removed fr... |
| `more_code_info` | string |  |
| `mri_safety` | string | Indicates the MRI Safety Information, if any, that is present in the device labeling. Please see the ASTM F2503-13 st... |
| `number_devices_in_event` | string | Number of devices noted in the adverse event report. Almost always `1`. May be empty if `report_source_code` contains... |
| `number_patients_in_event` | string | Number of patients noted in the adverse event report. Almost always `1`. May be empty if `report_source_code` contain... |
| `openfda.application_number` | array of strings |  |
| `openfda.brand_name` | array of strings |  |
| `openfda.dosage_form` | array of strings |  |
| `openfda.generic_name` | array of strings |  |
| `openfda.is_original_packager` | boolean |  |
| `openfda.manufacturer_name` | array of strings |  |
| `openfda.nui` | array of strings |  |
| `openfda.original_packager_product_ndc` | array of strings |  |
| `openfda.package_ndc` | array of strings |  |
| `openfda.pharm_class_cs` | array of strings |  |
| `openfda.pharm_class_epc` | array of strings |  |
| `openfda.pharm_class_moa` | array of strings |  |
| `openfda.pharm_class_pe` | array of strings |  |
| `openfda.pma_number` | string | FDA-assigned premarket application number, including leading letters. Leading letter “D” indicates Product Developmen... |
| `openfda.product_ndc` | array of strings |  |
| `openfda.product_type` | array of strings | The type of product being recalled. For device queries, this will always be `Devices`. |
| `openfda.route` | array of strings |  |
| `openfda.rxcui` | array of strings |  |
| `openfda.rxstring` | array of strings |  |
| `openfda.rxtty` | array of strings |  |
| `openfda.spl_id` | array of strings |  |
| `openfda.spl_set_id` | array of strings |  |
| `openfda.substance_name` | array of strings |  |
| `openfda.unii` | array of strings |  |
| `openfda.upc` | array of strings |  |
| `other_submission_description` | string | If 510(k) or PMA numbers are not applicable to the device recalled, the recall may contain other regulatory descripti... |
| `pan_agree` | string | Agreement between pan_result and antibody_truth. |
| `pan_result` | string | The test result for qualitative detection of Pan-Ig antibodies. |
| `pan_titer` | integer | The CDC spike titer for Pan-Ig in the sample. |
| `panel` | string | The testing program's unique identification of the panel of clinical samples against which the devices were tested. |
| `patient.date_received` | string | Date the report about this patient was received. |
| `patient.patient_age` | string | Patient's age. |
| `patient.patient_ethnicity` | string | Patient's ethnicity. |
| `patient.patient_problems` | array of strings | Describes actual adverse effects on the patient that may be related to the device problem observed during the reporte... |
| `patient.patient_race` | string | Patient's race. |
| `patient.patient_sequence_number` | string | Documentation forthcoming. |
| `patient.patient_sex` | string | Patient's gender. |
| `patient.patient_weight` | string | Patient's weight. |
| `patient.sequence_number_outcome` | array of strings | Outcome associated with the adverse event for this patient. Expect wide variability in this field; each string in the... |
| `patient.sequence_number_treatment` | array of strings | Treatment the patient received. |
| `pma_numbers` | array of strings | FDA-assigned premarket application number, including leading letters. Leading letter “D” indicates Product Developmen... |
| `premarket_submissions.submission_number` | string | Number associated with the regulatory decision regarding the applicant’s legal right to market a medical device for t... |
| `premarket_submissions.submission_type` | string | Indicates the premarket submission type. |
| `premarket_submissions.supplement_number` | string | Number assigned by FDA to a supplemental application for approval of a change in a medical device with an approved PMA. |
| `previous_use_code` | string | Whether the use of the suspect medical device was the initial use, reuse, or unknown. |
| `product_codes.code` | string | A three-letter identifier assigned to a device category |
| `product_codes.name` | string | Name associated with the three-letter Product Code |
| `product_codes.openfda` | object |  |
| `product_problem_flag` | string | Indicates whether or not a report was about the quality, performance or safety of a device. |
| `product_problems` | array of strings | The product problems that were reported to the FDA if there was a concern about the quality, authenticity, performanc... |
| `product_res_number` | string |  |
| `product_type` | string |  |
| `products.created_date` | string | Date listing was created (may be unreliable). |
| `products.exempt` | string | Flag indicating whether a device is exempt or not. |
| `products.openfda` | object |  |
| `products.owner_operator_number` | string | Number assigned to Owner Operator by CDRH. |
| `products.product_code` | string | A three-letter identifier assigned to a device category. Assignment is based upon the medical device classification d... |
| `proprietary_name` | array of strings | Proprietary or brand name or model number a product is marketed under. |
| `public_version_date` | date | Auto assigned the day file is generated with Time Stamp; All existing records will have first date assigned the day d... |
| `public_version_number` | string | Auto assigned version number, assigned just before file generation; All existing records will have version 1 assigned. |
| `public_version_status` | string | Definition forthcoming. |
| `publish_date` | date | Indicates the date the DI Record gets published and is available via Public Search. |
| `recall_initiation_date` | string | Date that the firm first began notifying the public or their consignees of the recall. |
| `recall_number` | string | A numerical designation assigned by FDA to a specific recall event used for tracking purposes. |
| `recall_status` | string | Current status of the recall. A record in the database is created when a firm initiates a correction or removal actio... |
| `record_key` | string | Current enhancements will allow the Primary DI to change after the DI record has been released to the public. To ensu... |
| `record_status` | string | Indicates the status of the DI Record. |
| `registration.address_line_1` | string | Facility or US agent address line 1. |
| `registration.address_line_2` | string | Facility or US agent address line 2. |
| `registration.city` | string | Facility or US agent city. |
| `registration.fei_number` | string | Facility identifier assigned to facility by the FDA Office of Regulatory Affairs. |
| `registration.initial_importer_flag` | string | Identifies whether facility is an initial importer. |
| `registration.iso_country_code` | string | Facility or US agent country code. |
| `registration.name` | string | Name associated with the facility or US agent. |
| `registration.owner_operator` | object |  |
| `registration.postal_code` | string | Facility foreign postal code. |
| `registration.reg_expiry_date_year` | string | Year that registration expires (expires 12/31 of that year). |
| `registration.registration_number` | string | Facility identifier assigned to facility by the FDA Office of Regulatory Affairs. |
| `registration.state_code` | string | Facility or US agent US state or foreign state or province. |
| `registration.status_code` | string | Registration status code. |
| `registration.us_agent` | object |  |
| `registration.zip_code` | string | Facility or US agent Zip code. |
| `regulation_number` | string | The classification regulation in the Code of Federal Regulations (CFR) under which the device is identified, describe... |
| `remedial_action` | array of strings | Follow-up actions taken by the device manufacturer at the time of the report submission, if applicable. |
| `removal_correction_number` | string | If a corrective action was reported to FDA under <a href='http://www.law.cornell.edu/uscode/text/21/360i'>21 USC 360i... |
| `report_number` | string | Identifying number for the adverse event report. The format varies, according to the source of the report. The field ... |
| `report_source_code` | string | Source of the adverse event report |
| `report_to_fda` | string | Whether the report was sent to the FDA by a user facility or importer (distributor). User facilities are required to ... |
| `report_to_manufacturer` | string | Whether the report was sent to the manufacturer by a user facility or importer (distributor). User facilities are req... |
| `reporter_occupation_code` | string | Initial reporter occupation. |
| `reprocessed_and_reused_flag` | string | Indicates whether the suspect device was a single-use device that was reprocessed and reused on a patient. |
| `res_event_number` | string | A five digit, numerical designation assigned by FDA to a specific recall event used for tracking purposes. |
| `review_advisory_committee` | string | Known as the “510(k) Review Panel” since 2014, this helps define the review division within CDRH in which the 510(k) ... |
| `review_code` | string | Documentation forthcoming. |
| `review_panel` | string | Known as the “510(k) Review Panel” since 2014, this helps define the review division within CDRH in which the 510(k) ... |
| `root_cause_description` | string | FDA determined general type of recall cause. Per FDA policy, recall cause determinations are subject to modification ... |
| `sample_id` | string | The unique ID of the sample in the panel. |
| `sample_no` | integer | The sequence in which the sample was tested. |
| `single_use_flag` | string | Whether the device was labeled for single use or not. |
| `source_type` | array of strings | The manufacturer-reported source of the adverse event report. |
| `statement_or_summary` | string | A statement or summary can be provided per 21 CFR 807.3(n) and (o). A 510(k) summary, submitted under section 513(i) ... |
| `status` | string |  |
| `sterilization.is_sterile` | boolean | Indicates the medical device is free from viable microorganisms. See ISO/TS 11139. |
| `sterilization.is_sterilization_prior_use` | boolean | Indicates that the device requires sterilization prior to use. |
| `sterilization.sterilization_methods` | string | Indicates the method(s) of sterilization that can be used for this device. |
| `storage.high` | object |  |
| `storage.low` | object |  |
| `storage.special_conditions` | string | Indicates any special storage requirements for the device. |
| `storage.type` | string | Indicates storage and handling requirements for the device including temperature, humidity, and atmospheric pressure. |
| `street_1` | string | Delivery address of the applicant. |
| `street_2` | string | Delivery address of the applicant. |
| `submission_type_id` | string | The submission type (510(k), PMA, 510(k) Exempt) to which a product code is limited, or “Contact ODE” if its limitati... |
| `summary_malfunction_reporting` | string | The Voluntary Malfunction Summary Reporting Program allows participating companies to submit certain medical device m... |
| `supplement_number` | string | FDA assigned supplement number. |
| `supplement_reason` | string | General description for the reason for the supplement or application. |
| `supplement_type` | string | [Link to general criteria used for PMA regulation](http://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.... |
| `termination_date` | string |  |
| `trade_name` | string | This is the proprietary name of the approved device. |
| `type` | string | The sample material. |
| `type_of_report` | array of strings | The type of report. |
| `unclassified_reason` | string | This indicates the reason why a device is unclassified (e.g. Pre-Amendment). |
| `version_or_model_number` | string | The version or model found on the device label or accompanying packaging used to identify a category or design of a d... |
| `voluntary_mandated` | string | Describes who initiated the recall. Recalls are almost always voluntary, meaning initiated by a firm. A recall is dee... |
| `zip` | string | Portion of address that designates the zip code of the applicant. |
| `zip_code` | string | Portion of address that designates the U.S. zip code of applicant. |
| `zip_ext` | string | Portion of address that designates the “speed zip” or the “+4” of the applicant. |

## 2. device/udi (UDI/GUDID)

**20 fields**

| Field | Type | Description |
|-------|------|-------------|
| `advisory_committee` | string | Code under which the product was originally classified, based on the product code. This is a historical designation f... |
| `advisory_committee_description` | string | Full spelling of the Advisory Committee abbreviation (e.g. Gastroenterology and Urology Devices Panel of the Medical ... |
| `applicant` | string | The manufacturer of record or third party who submits a 510(k) submission. Also known as sponsor. Please note, before... |
| `code_info` | string | A list of all lot and/or serial numbers, product numbers, packer or manufacturer numbers, sell or use by dates, etc.,... |
| `country` | string | The country in which the recalling firm is located. |
| `decision_code` | string | Four letter codes that denote the specific substantial equivalence decision rendered by FDA on a specific 510(k). |
| `decision_date` | string | This is the date on which FDA rendered a final decision on a 510(k) submission. |
| `device_name` | string | This is the proprietary name, or trade name, of the cleared device |
| `distribution_pattern` | string | General area of initial distribution such as, “Distributors in 6 states: NY, VA, TX, GA, FL and MA; the Virgin Island... |
| `expedited_review_flag` | string | Qualifying products are eligible for ‘priority review’ by CDRH in one of four possible review tracks if it is intende... |
| `k_number` | string | FDA-assigned premarket notification number, including leading letters. Leading letters “BK” indicates 510(k) clearanc... |
| `openfda.k_number` | array of strings | FDA-assigned premarket notification number, including leading letters. Leading letters “BK” indicates 510(k) clearanc... |
| `pma_number` | string | FDA-assigned premarket application number, including leading letters. Leading letter “D” indicates Product Developmen... |
| `postal_code` | string | A series of letters and/or digits, sometimes including spaces or punctuation, included in a postal address for the pu... |
| `product_description` | string | Brief description of the product being recalled. |
| `product_quantity` | string | The amount of defective product subject to recall. |
| `reason_for_recall` | string | Information describing how the product is defective and violates the FD&C Act or related statutes. |
| `recalling_firm` | string | The firm that initiates a recall or, in the case of an FDA requested recall or FDA mandated recall, the firm that has... |
| `report_date` | string | Date that the FDA issued the enforcement report for the product recall. |
| `third_party_flag` | string | Eligibility for a manufacturer to utilize a contracted Accredited Person in lieu of direct submission to FDA. By law,... |

## 3. device/510k (510(k) Clearances)

**12 fields**

| Field | Type | Description |
|-------|------|-------------|
| `address_1` | string | Delivery address of the applicant. |
| `address_2` | string | Delivery address of the applicant. |
| `date_received` | string | Date that the FDA Document Control Center received the submission. |
| `meta.disclaimer` | string | Important details notes about openFDA data and limitations of the dataset. |
| `meta.last_updated` | string | The last date when this openFDA endpoint was updated. Note that this does not correspond to the most recent record fo... |
| `meta.license` | string | Link to a web page with license terms that govern data within openFDA. |
| `meta.results` | object |  |
| `meta.type` | unknown |  |
| `openfda.device_class` | string | A risk based classification system for all medical devices ((Federal Food, Drug, and Cosmetic Act, section 513) |
| `openfda.device_name` | string | This is the proprietary name, or trade name, of the cleared device. |
| `openfda.medical_specialty_description` | string | Regulation Medical Specialty is assigned based on the regulation (e.g. 21 CFR Part 888 is Orthopedic Devices) which i... |
| `openfda.regulation_number` | array of strings | The classification regulation in the Code of Federal Regulations (CFR) under which the device is identified, describe... |

## 4. device/registrationlisting (Registration & Listing)

**4 fields**

| Field | Type | Description |
|-------|------|-------------|
| `city` | string | City of the delivery address of the applicant. |
| `openfda.fei_number` | array of strings | Facility identifier assigned to facility by the FDA Office of Regulatory Affairs. |
| `openfda.registration_number` | array of strings | Facility identifier assigned to facility by the FDA Office of Regulatory Affairs. |
| `state` | string | This is the state of record of U.S. based applicants. |

## 5. device/classification (Device Classification)

**1 fields**

| Field | Type | Description |
|-------|------|-------------|
| `product_code` | string | A three-letter identifier assigned to a device category. Assignment is based upon the medical device classification d... |
