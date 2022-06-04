-- :name remove_specific_insurance_choice :affected
DELETE FROM out_of_net_services_for WHERE insurance_name = :insurance_name AND user_id = :user_id