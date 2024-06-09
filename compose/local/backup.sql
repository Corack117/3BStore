--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.1

-- Started on 2024-06-08 18:17:15 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 3504 (class 0 OID 74198)
-- Dependencies: 225
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, slug, email) FROM stdin;
pbkdf2_sha256$720000$eNbAzb97nzC660TV98eO4T$CjkgGKzD0tEF5De5HUQ0C2TUvjQS5AuPjYaK+JxcBLw=	\N	f	mortel	Marcos	Ordaz	f	t	2024-06-09 00:13:49.750987+00	883fec8d-ba51-4da5-b781-00ac40241692	mortel@gmail.com
pbkdf2_sha256$720000$pUPdfGjhOePOITQDKFcGmv$nsajfUUVjhFVakIPyq6/gmyZaer9GyTZoCYVNuonPmQ=	\N	f	corack	Sergio	Ordaz	t	t	2024-06-09 00:13:31.814841+00	11cd4f32-0618-4483-b3ab-3826370f233b	orcheko@gmail.com
\.


COPY public.orders_order (slug, num_products, total, active, created, updated, user_id) FROM stdin;
\.


--
-- TOC entry 3513 (class 0 OID 74289)
-- Dependencies: 234
-- Data for Name: orders_orderdetail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_orderdetail (slug, quantity, unit_price, active, created, updated, order_id, product_id) FROM stdin;
\.


--
-- TOC entry 3514 (class 0 OID 74296)
-- Dependencies: 235
-- Data for Name: orders_productreturn; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_productreturn (slug, quantity, refunded_amount, active, created, updated, order_id, product_id) FROM stdin;
\.


--
-- TOC entry 3511 (class 0 OID 74272)
-- Dependencies: 232
-- Data for Name: products_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products_product (slug, sku, name, description, price, stock, active, created, updated) FROM stdin;
6ed62caa-fba2-4d4a-b5da-1cf95d60ed5e	EXAMPLE-SKU-001	Aceite de oliva Mar Amargo	Aceite de oliva marca Mar Amargo, tamaño 500ml	1530	15	t	2024-06-08 15:35:46.697288+00	2024-06-08 15:35:46.697297+00
b22646cd-4ce9-44e2-a4b9-22f64ec64edb	EXAMPLE-SKU-002	Shampoo Herbal	Shampoo de hierbas naturales, tamaño 250ml	800	20	t	2024-06-08 18:56:19.111288+00	2024-06-08 18:56:19.111299+00
67d171d4-8ac4-44d8-b504-2912e2e455b5	EXAMPLE-SKU-003	Gel de ducha refrescante	Gel de ducha con fragancia refrescante, tamaño 500ml	1200	10	t	2024-06-08 18:56:29.439314+00	2024-06-08 18:56:29.439331+00
d0d85998-f229-492f-8428-0ebfd53aada1	EXAMPLE-SKU-004	Jabón de manos antibacterial	Jabón de manos con propiedades antibacterianas, tamaño 150ml	550	30	t	2024-06-08 18:56:39.039528+00	2024-06-08 18:56:39.039541+00
c26f58be-80f4-40a9-a48b-8ac4960d39b8	EXAMPLE-SKU-005	Crema hidratante facial	Crema hidratante para el rostro, tamaño 50ml	2000	8	t	2024-06-08 18:56:47.000637+00	2024-06-08 18:56:47.000644+00
1d401655-9d3b-4a2e-847f-60d01439ce66	EXAMPLE-SKU-006	Protector solar FPS 50+	Protector solar con factor de protección solar (FPS) 50+, tamaño 100ml	1800	12	t	2024-06-08 18:57:00.01381+00	2024-06-08 18:57:00.013817+00
046d2b53-b353-4abf-b784-b69082260bb0	EXAMPLE-SKU-007	Desodorante roll-on para hombres	Desodorante roll-on para hombres, tamaño 50ml	700	25	t	2024-06-08 18:57:13.899679+00	2024-06-08 18:57:13.899686+00
84c222df-e455-40b7-909e-b19bf1970659	EXAMPLE-SKU-008	Perfume floral primaveral	Perfume con fragancia floral para la primavera, tamaño 30ml	2500	5	t	2024-06-08 18:57:22.296247+00	2024-06-08 18:57:22.296261+00
5ae9ecc5-8c75-42ae-ad40-a0bf310f79ab	EXAMPLE-SKU-009	Aceite de coco virgen	Aceite de coco virgen prensado en frío, tamaño 500ml	1600	18	t	2024-06-08 18:57:29.627046+00	2024-06-08 18:57:29.627067+00
fbc6f73c-4f49-475f-b589-235a8019a9e5	EXAMPLE-SKU-010	Pasta de dientes blanqueadora	Pasta de dientes con fórmula blanqueadora, tamaño 100g	900	22	t	2024-06-08 18:57:34.572795+00	2024-06-08 18:57:34.572809+00
\.
