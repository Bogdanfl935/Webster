-- Creation of function that checks for duplicates in parsed_urls and visited_urls
CREATE FUNCTION verify_duplicate()
    RETURNS trigger AS
$BODY$
BEGIN
    IF EXISTS(SELECT 1 FROM next_links WHERE new.url = url) THEN
        RETURN NULL;
    END IF;

    IF EXISTS(SELECT 1 FROM visited_links WHERE new.url = url) THEN
        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

CREATE TRIGGER verify_duplicate_next_links
    BEFORE INSERT
    ON parsed_urls
    FOR EACH ROW
EXECUTE PROCEDURE verify_duplicate();