-- CREATE VIEW mpga.club_overview AS
SELECT
   mc.id
  ,mc.name
  ,mc.type_2
  ,r.reg_year
  ,CASE WHEN r.reg_year = r.current_year THEN 1 ELSE 0 END AS is_current
  ,p.president
  ,CASE WHEN LENGTH(p.president) > 1 THEN 1 ELSE 0 END AS has_president
  ,c1.contact_name AS primary_mc_contact
  ,CASE WHEN c1.contact_name IS NOT NULL THEN 1 ELSE 0 END AS has_mc_contact
  ,c2.contact_name AS primary_fac_contact
  ,CASE WHEN c2.contact_name IS NOT NULL THEN 1 ELSE 0 END AS has_fac_contact
FROM mpga.clubs_club mc
JOIN (	
    SELECT mc.id, MAX(m.`year`) AS reg_year, YEAR(sysdate()) AS current_year
	FROM mpga.clubs_club mc
	LEFT JOIN mpga.clubs_membership m ON mc.id = m.club_id
	GROUP BY mc.id
) r ON mc.id = r.id
JOIN (	
    SELECT mc.id, CONCAT_WS(' ', c.first_name, c.last_name) AS president
	FROM mpga.clubs_club mc
	LEFT JOIN mpga.clubs_clubcontact cc ON mc.id = cc.club_id AND cc.`role` LIKE '%President'
	LEFT JOIN mpga.clubs_contact c ON cc.contact_id = c.id
) p ON mc.id = p.id
JOIN (	
    SELECT mc.id, c1_sub.contact_name
	FROM mpga.clubs_club mc
	LEFT JOIN (
		SELECT cc.club_id, CONCAT_WS(' ', c.first_name, c.last_name) AS contact_name
		FROM mpga.clubs_clubcontact cc
		JOIN mpga.clubs_contact c ON cc.contact_id = c.id
		WHERE cc.is_primary = 1
		AND c.contact_type = 'MC'
	) c1_sub ON mc.id = c1_sub.club_id
) c1 ON mc.id = c1.id
JOIN (	
    SELECT mc.id, c2_sub.contact_name
	FROM mpga.clubs_club mc
	LEFT JOIN (
		SELECT cc.club_id, CONCAT_WS(' ', c.first_name, c.last_name) AS contact_name
		FROM mpga.clubs_clubcontact cc
		JOIN mpga.clubs_contact c ON cc.contact_id = c.id
		WHERE cc.is_primary = 1
		AND c.contact_type <> 'MC'
	) c2_sub ON mc.id = c2_sub.club_id
) c2 ON mc.id = c2.id
