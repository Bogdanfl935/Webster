--====================[Default roles available within motorage application]====================
INSERT INTO Role(title) VALUES ('ROLE_USER') ON CONFLICT (title) DO NOTHING;
INSERT INTO Role(title) VALUES ('ROLE_ADMIN') ON CONFLICT (title) DO NOTHING;