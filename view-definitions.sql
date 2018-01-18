ALTER VIEW mpga.team_captains_view AS
SELECT
   cl.name
  ,co.first_name
  ,co.last_name
  ,co.email
  ,co.primary_phone
  ,co.alternate_phone
  ,co.contact_type
  ,t.is_senior
  ,t.group_name
  ,t.`year`
  ,CONCAT_WS('-', cl.id, co.id, t.id) AS vkey
FROM mpga.clubs_club cl
JOIN mpga.clubs_team t ON cl.id = t.club_id
JOIN mpga.clubs_contact co ON t.contact_id = co.id;

ALTER VIEW mpga.club_contacts_view AS
SELECT
   cl.name
  ,co.first_name
  ,co.last_name
  ,co.email
  ,co.primary_phone
  ,co.alternate_phone
  ,co.contact_type
  ,cc.is_primary
  ,cc.`role`
  ,CONCAT_WS('-', cl.id, co.id, cc.id) AS vkey
FROM mpga.clubs_club cl
JOIN mpga.clubs_clubcontact cc ON cl.id = cc.club_id
JOIN mpga.clubs_contact co ON cc.contact_id = co.id
WHERE cc.`role` <> 'Handicap Chair';

ALTER VIEW mpga.all_contacts_view AS
SELECT
   name
  ,first_name
  ,last_name
  ,email
  ,primary_phone
  ,alternate_phone
  ,contact_type
  ,is_primary
  ,`role`
  ,vkey
FROM mpga.club_contacts_view
UNION
SELECT
   name
  ,first_name
  ,last_name
  ,email
  ,primary_phone
  ,alternate_phone
  ,contact_type
  ,0
  ,CASE WHEN is_senior = 0 THEN 'Match Play Captain' ELSE 'Sr. Match Play Captain' END
  ,vkey
FROM mpga.team_captains_view
WHERE `year` = (SELECT MAX(`year`) FROM mpga.clubs_team);

ALTER VIEW mpga.club_handicap_chairs_view AS
SELECT
   cl.name
  ,co.first_name
  ,co.last_name
  ,co.email
  ,co.primary_phone
  ,co.alternate_phone
  ,co.contact_type
  ,CONCAT_WS('-', cl.id, co.id, cc.id) AS vkey
FROM mpga.clubs_club cl
JOIN mpga.clubs_clubcontact cc ON cl.id = cc.club_id
JOIN mpga.clubs_contact co ON cc.contact_id = co.id
WHERE cc.`role` = 'Handicap Chair';