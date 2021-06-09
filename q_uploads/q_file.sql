    INSERT INTO CCWD.suppliers (


    SELECT
        cs.e_supplierName,
        cs.phone,
        cs.addressLine1,
        cs.addressLine2,
        cs.city,
        cs.state ,
        cs.postalCode,
        cs.country,
		cs.e_pin,
        cs.customerNumber
    FROM
        CCWD.customers as CS
    JOIN CCWD.names as nm
    on nm.as=cs.as
    WHERE
        cd.country = 'USA' AND
        cd.state = 'CA';



    UPDATE CCWD.manager
    SET status = 'Y'
    WHERE branch_id IN
    (
      select branch_id
      FROM (select * from CCWD.du_manager) AS m2
      WHERE (branch_id, year) IN
      (
        SELECT branch_id, year
        FROM CCWD.branch_master
        WHERE type = 'finance'
      )
    ));


    INSERT INTO CCWD.courses(
    SELECT c.name, c.location,c.fees
    FROM   course c
    WHERE  c.cid = 2);

    INSERT INTO CCWD.Results (
       SELECT d.id, name
       FROM Names f
       JOIN People d ON d.id  = f.id
       where d.mid is not null);

    INSERT INTO CCWD.physician (
    SELECT
        to.id,
		to.e_first_name,
        to.full_name,
        to.address,
        to.total
    FROM
        CCWD.total_orders as to
    join Temp as tm
    on tm.od=to.od
    WHERE
        total > 10000);