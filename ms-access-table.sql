-- Dues
select c.name, c.website, case when m.club_id is not null then 100.00 else null end, m.notes, m.payment_code, m.payment_date
from `mpgagolf$mpga`.clubs_club as c
left join `mpgagolf$mpga`.clubs_membership as m on c.id = m.club_id and m.`year` = 2018
where c.id <> 25
order by c.name

-- CY Contact
SELECT c.name, CONCAT_WS(' ', sub.first_name, sub.last_name), sub.role, sub.primary_phone, sub.alternate_phone, sub.email
from `mpgagolf$mpga`.clubs_club as c
left join (
   select *
   from `mpgagolf$mpga`.club_contacts_view as v
   where is_primary = 1
   and contact_type = 'Men''s Club'
   UNION
   select *
   from `mpgagolf$mpga`.club_contacts_view as v
   where is_primary = 1
   and contact_type = 'Facilities'
	and name not in (select name from `mpgagolf$mpga`.club_contacts_view where is_primary = 1 and contact_type = 'Men''s Club')
) sub on c.name = sub.name
where c.id <> 25
order by c.name

-- CY President
SELECT c.name, CONCAT_WS(' ', sub.first_name, sub.last_name), sub.primary_phone, sub.alternate_phone, sub.email
from `mpgagolf$mpga`.clubs_club as c
left join (
   select *
   from `mpgagolf$mpga`.club_contacts_view as v
   where role = 'Men''s Club President'
) sub on c.name = sub.name
where c.id <> 25
order by c.name

-- CY Match Play
SELECT c.name, CONCAT_WS(' ', sub.first_name, sub.last_name), sub.primary_phone, sub.alternate_phone, sub.email, sub.group_name
from `mpgagolf$mpga`.clubs_club as c
left join (
   select *
   from `mpgagolf$mpga`.team_captains_view
   where is_senior = 0
   and year = 2018
) sub on c.name = sub.name
where c.id <> 25
order by c.name

SELECT c.name, CONCAT_WS(' ', sub.first_name, sub.last_name), sub.primary_phone, sub.alternate_phone, sub.email, sub.group_name
from `mpgagolf$mpga`.clubs_club as c
left join (
   select *
   from `mpgagolf$mpga`.team_captains_view
   where is_senior = 1
   and year = 2018
) sub on c.name = sub.name
where c.id <> 25
order by c.name

-- HC
SELECT c.name, CONCAT_WS(' ', sub.first_name, sub.last_name), sub.role, c.address_txt, c.city, c.state, c.zip, c.club_phone, c.club_email, c.website
from `mpgagolf$mpga`.clubs_club as c
left join (
   select *
   from `mpgagolf$mpga`.club_contacts_view as v
   where is_primary = 1
   and contact_type = 'Facilities'
) sub on c.name = sub.name
where c.id <> 25
order by c.name
