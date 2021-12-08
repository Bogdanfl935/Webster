-- Creation of function that checks for
CREATE FUNCTION verify_duplicate()
    RETURNS trigger AS
$BODY$
BEGIN
    IF EXISTS(SELECT 1 FROM next_links WHERE new.url_site = url_site) THEN
        RETURN NULL;
    ELSE
        RETURN NEW;
    END IF;
END;
$BODY$
    LANGUAGE plpgsql;

CREATE TRIGGER verify_duplicate_next_links
    BEFORE INSERT
    ON next_links
    FOR EACH ROW
EXECUTE PROCEDURE verify_duplicate();
