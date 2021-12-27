-- Creation of function that checks for duplicates in parsed_urls and visited_urls
CREATE FUNCTION verify_duplicate()
    RETURNS trigger AS
$BODY$
BEGIN
    IF EXISTS(SELECT 1 FROM parsed_url WHERE new.url = url) THEN
        RAISE EXCEPTION 'URL already exists in parsed_url';
    END IF;

    IF EXISTS(SELECT 1 FROM visited_url WHERE new.url = url) THEN
        RAISE EXCEPTION 'URL already exists in visited_url';
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

CREATE TRIGGER verify_duplicate_next_urls BEFORE INSERT ON parsed_url FOR EACH ROW EXECUTE PROCEDURE verify_duplicate();


CREATE FUNCTION verify_foreign_table_reference()
    RETURNS trigger AS
$BODY$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM user_record WHERE id = new.user_id) THEN
        RAISE EXCEPTION 'Id does not exist';
    END IF;

    RETURN NEW;
END;
$BODY$
    LANGUAGE plpgsql;

DO $$
DECLARE
    iterator text;
BEGIN
    FOR iterator IN SELECT table_name FROM information_schema.columns WHERE column_name = 'user_id'
    LOOP
        EXECUTE format('CREATE TRIGGER verify_foreign_table_references
                        BEFORE INSERT ON %I FOR EACH ROW EXECUTE PROCEDURE verify_foreign_table_reference()',
                        iterator);
    END LOOP;
END;
$$ LANGUAGE plpgsql;