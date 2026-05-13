import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

st.set_page_config(page_title="Gas & Strompreise Vergleich 2020-2025", layout="wide")

st.title("Gas- & Strompreise für Haushaltskunden 2020–2025")
st.markdown("**Vergleich von Gas- und Strompreisen** (inkl. Steuern & Abgaben) in €/kWh – Halbjahreswerte")

# ── Gaspreise (vollständiger Datensatz) ─────────────────────────────────────
gas_csv = """Unit;Tax;Currency;Geo;Time period;€/kWh;EU?
Kilowatt-hour;All taxes and levies included;Euro;Austria;2020-S2;0.0656;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S1;0.0636;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S2;0.0695;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S1;0.0767;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S2;0.1235;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S1;0.1560;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S2;0.1477;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S1;0.1379;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S2;0.1237;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Austria;2025-S1;0.1220;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2020-S2;0.0498;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S1;0.0468;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S2;0.0676;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S1;0.0943;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S2;0.1363;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S1;0.1146;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S2;0.0994;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S1;0.0801;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S2;0.0903;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Belgium;2025-S1;0.0919;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2020-S2;0.0348;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S1;0.0368;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S2;0.0708;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S1;0.0764;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S2;0.1173;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S1;0.0879;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S2;0.0703;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S1;0.0619;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S2;0.0649;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2025-S1;0.0765;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2020-S2;0.0558;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S1;0.0562;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S2;0.0554;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S1;0.0696;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S2;0.1066;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S1;0.1138;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S2;0.1125;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S1;0.1085;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S2;0.1029;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Czechia;2025-S1;0.0967;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2020-S2;0.0620;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S1;0.0647;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S2;0.0692;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S1;0.0806;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S2;0.0941;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S1;0.1230;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S2;0.1145;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S1;0.1198;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S2;0.1238;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Germany;2025-S1;0.1216;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2020-S2;0.0747;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S1;0.0895;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S2;0.1247;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S1;0.1509;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S2;0.2084;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S1;0.1655;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S2;0.1220;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S1;0.1223;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S2;0.1313;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Denmark;2025-S1;0.1306;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2020-S2;0.0411;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S1;0.0435;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S2;0.0750;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S1;0.1106;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S2;0.1089;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S1;0.1099;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S2;0.0791;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S2;0.0788;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Estonia;2025-S1;0.0856;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2020-S2;0.0517;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S1;0.0449;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S2;0.1014;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S1;0.0821;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S2;0.1599;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S1;0.1187;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S2;0.0926;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S1;0.0744;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S2;0.0945;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Greece;2025-S1;0.0863;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2020-S2;0.0890;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S2;0.1082;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S1;0.0897;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S2;0.1574;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S1;0.1077;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S2;0.1010;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S1;0.0858;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S2;0.0901;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Spain;2025-S1;0.0859;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2020-S2;0.0751;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2021-S2;0.0788;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S1;0.0859;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2022-S2;0.1008;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S1;0.1044;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2023-S2;0.1181;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S1;0.1197;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2024-S2;0.1331;WAHR
Kilowatt-hour;All taxes and levies included;Euro;France;2025-S1;0.1298;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2020-S2;0.0377;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S1;0.0374;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S2;0.0398;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S1;0.0412;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S2;0.0450;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S1;0.0443;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S2;0.0457;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S1;0.0447;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S2;0.0456;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Croatia;2025-S1;0.0461;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2020-S2;0.0308;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S1;0.0307;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S2;0.0305;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S1;0.0291;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S2;0.0349;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S1;0.0337;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S2;0.0335;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S1;0.0275;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S2;0.0315;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Hungary;2025-S1;0.0307;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2020-S2;0.0702;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S1;0.0620;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S2;0.0783;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S1;0.0847;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S2;0.1544;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S1;0.1465;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S2;0.1638;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S1;0.1271;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S2;0.1347;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Ireland;2025-S1;0.1218;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2020-S2;0.0897;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S1;0.0703;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S2;0.1005;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S1;0.0986;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S2;0.1310;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S1;0.0981;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S2;0.1347;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S1;0.1140;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S2;0.1586;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Italy;2025-S1;0.1240;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2020-S2;0.0295;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S1;0.0279;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S2;0.0410;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S1;0.0587;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S2;0.1288;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S1;0.1849;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S2;0.1454;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S1;0.0739;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S2;0.0596;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2025-S1;0.0667;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2020-S2;0.0366;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S1;0.0438;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S2;0.0639;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S1;0.0856;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S2;0.0891;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S1;0.0875;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S2;0.0850;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S1;0.0883;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S2;0.0732;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2025-S1;0.0929;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2020-S2;0.0280;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S1;0.0297;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S2;0.0432;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S1;0.0462;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S2;0.1111;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S1;0.1105;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S2;0.0901;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S1;0.0923;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S2;0.0880;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Latvia;2025-S1;0.0832;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2020-S2;0.1084;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S1;0.1005;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S2;0.1167;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S1;0.1287;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S2;0.1923;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S1;0.1953;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S2;0.1548;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S1;0.1647;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S2;0.1698;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2025-S1;0.1617;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2020-S2;0.0419;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S1;0.0376;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S2;0.0473;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S1;0.0549;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S2;0.0553;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S1;0.0683;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S2;0.0730;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2020-S2;0.0783;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S1;0.0762;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S2;0.0773;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S1;0.0837;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S2;0.1277;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S1;0.1406;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S2;0.1374;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S1;0.1192;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S2;0.1366;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Portugal;2025-S1;0.1265;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2020-S2;0.0320;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S1;0.0317;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S2;0.0475;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S1;0.0611;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S2;0.1265;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S1;0.0548;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S2;0.0558;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S1;0.0581;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S2;0.0541;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Romania;2025-S1;0.0559;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2020-S2;0.1422;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S1;0.1438;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S2;0.2058;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S1;0.2216;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S2;0.2751;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S1;0.2189;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S2;0.2070;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S1;0.1760;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S2;0.1893;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Sweden;2025-S1;0.2128;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2020-S2;0.0549;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S1;0.0547;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S2;0.0587;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S1;0.0691;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S2;0.0942;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S1;0.0971;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S2;0.1107;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S1;0.0972;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S2;0.0909;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2025-S1;0.0849;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2020-S2;0.0480;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S1;0.0411;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S2;0.0423;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S1;0.0488;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S2;0.0499;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S1;0.0571;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S2;0.0611;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S1;0.0585;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S2;0.0600;WAHR
Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2025-S1;0.0587;WAHR"""

# ── Strompreise (Elektrizität) ────────────────────────────────────────────
strom_csv = """Energie;Unit;Tax;Currency;Geo;Zeit;Preis
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2021-S2;0.2252
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S1;0.2200
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2022-S2;0.2356
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S1;0.2720
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2023-S2;0.2885
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S1;0.2846
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2024-S2;0.2578
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2025-S1;0.2960
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Austria;2025-S2;0.3287
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2021-S2;0.3002
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S1;0.3478
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2022-S2;0.4519
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S1;0.4318
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2023-S2;0.3772
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S1;0.3346
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2024-S2;0.3338
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2025-S1;0.3574
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Belgium;2025-S2;0.3554
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2021-S2;0.1091
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S1;0.1091
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2022-S2;0.1149
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S1;0.1136
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2023-S2;0.1194
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S1;0.1185
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2024-S2;0.1215
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2025-S1;0.1295
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Bulgaria;2025-S2;0.1353
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2021-S2;0.1871
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S1;0.2317
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2022-S2;0.1572
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S1;0.3041
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2023-S2;0.3039
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S1;0.3259
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2024-S2;0.3199
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2025-S1;0.3074
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Czechia;2025-S2;0.3107
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2021-S2;0.3288
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S1;0.3348
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2022-S2;0.3475
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S1;0.4230
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2023-S2;0.4162
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S1;0.4100
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2024-S2;0.4111
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2025-S1;0.4001
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Germany;2025-S2;0.4042
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2021-S2;0.2873
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S1;0.3958
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2022-S2;0.5370
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S1;0.3779
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2023-S2;0.3076
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S1;0.3189
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2024-S2;0.3244
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2025-S1;0.3019
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Denmark;2025-S2;0.2847
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2021-S2;0.1960
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S1;0.2031
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2022-S2;0.2381
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S1;0.2081
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2023-S2;0.2192
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S1;0.2155
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2024-S2;0.2107
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2025-S1;0.2158
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Estonia;2025-S2;0.2124
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2021-S2;0.2086
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S1;0.2339
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2022-S2;0.2591
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S1;0.2486
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2023-S2;0.2463
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S1;0.2434
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2024-S2;0.2493
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2025-S1;0.2563
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Greece;2025-S2;0.2552
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2021-S2;0.2878
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S1;0.3207
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2022-S2;0.3452
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S1;0.2647
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2023-S2;0.2552
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S1;0.2688
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2024-S2;0.2643
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2025-S1;0.2841
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Spain;2025-S2;0.2872
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2021-S2;0.1970
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2022-S1;0.2046
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2022-S2;0.2106
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2023-S1;0.2225
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2023-S2;0.2512
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2024-S1;0.2758
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2024-S2;0.2850
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2025-S1;0.2602
Electricity;Kilowatt-hour;All taxes and levies included;Euro;France;2025-S2;0.2479
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2021-S2;0.1325
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S1;0.1377
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2022-S2;0.1493
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S1;0.1557
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2023-S2;0.1543
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S1;0.1540
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2024-S2;0.1530
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2025-S1;0.1691
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Croatia;2025-S2;0.1710
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S1;0.1006
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2021-S2;0.1007
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S1;0.0946
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2022-S2;0.1092
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S1;0.1181
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2023-S2;0.1109
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S1;0.1090
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2024-S2;0.1056
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2025-S1;0.1066
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Hungary;2025-S2;0.1126
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2020-S2;0.2505
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S1;0.2453
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2021-S2;0.2799
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S1;0.2283
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2022-S2;0.3170
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S1;0.2739
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2023-S2;0.3746
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S1;0.2592
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2024-S2;0.3049
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Ireland;2025-S2;0.3821
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2021-S2;0.2613
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S1;0.3359
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2022-S2;0.3923
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S1;0.4068
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2023-S2;0.3619
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S1;0.3621
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2024-S2;0.3505
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2025-S1;0.3735
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Italy;2025-S2;0.3330
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2021-S2;0.1501
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S1;0.1513
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2022-S2;0.2474
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S1;0.2917
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2023-S2;0.2313
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S1;0.2368
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2024-S2;0.2235
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2025-S1;0.2190
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Lithuania;2025-S2;0.2075
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2021-S2;0.1901
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S1;0.1928
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2022-S2;0.1945
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S1;0.1887
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2023-S2;0.1909
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2024-S1;0.1925
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Luxembourg;2025-S2;0.2610
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2021-S2;0.1961
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S1;0.1763
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2022-S2;0.3014
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S1;0.3161
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2023-S2;0.3040
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S1;0.2584
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2024-S2;0.2429
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2025-S1;0.2675
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Latvia;2025-S2;0.2650
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2020-S2;0.1273
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S1;0.1246
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2021-S2;0.1367
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S1;0.0118
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2022-S2;0.1075
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S1;0.3491
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2023-S2;0.2187
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S1;0.2407
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2024-S2;0.1974
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2025-S1;0.2335
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Netherlands;2025-S2;0.2483
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2021-S2;0.1654
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S1;0.1530
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2022-S2;0.1709
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S1;0.1979
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2023-S2;0.2291
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2024-S2;0.2573
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Poland;2025-S2;0.2854
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2021-S2;0.2285
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S1;0.2320
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2022-S2;0.2347
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S1;0.2196
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2023-S2;0.2395
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2024-S2;0.2764
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2025-S1;0.2577
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Portugal;2025-S2;0.2582
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2021-S2;0.1611
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S1;0.2320
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2022-S2;0.3421
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S1;0.1800
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2023-S2;0.1782
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S1;0.1774
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2024-S2;0.1748
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2025-S1;0.1796
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Romania;2025-S2;0.2907
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2020-S2;0.1650
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S1;0.1697
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2021-S2;0.2053
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S1;0.1781
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2022-S2;0.2227
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S1;0.2172
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2023-S2;0.1870
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S1;0.2043
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2024-S2;0.1939
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2025-S1;0.2133
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Sweden;2025-S2;0.2195
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2021-S2;0.1638
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S1;0.1344
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2022-S2;0.1886
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S1;0.1872
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2023-S2;0.2062
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S1;0.2074
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2024-S2;0.1964
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2025-S1;0.1807
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovenia;2025-S2;0.2100
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2021-S2;0.1629
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S1;0.1793
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2022-S2;0.1891
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S1;0.1907
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2023-S2;0.1967
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S1;0.1808
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2024-S2;0.1791
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2025-S1;0.1892
Electricity;Kilowatt-hour;All taxes and levies included;Euro;Slovakia;2025-S2;0.1880"""

@st.cache_data
def load_data():
    # Gas laden
    gas = pd.read_csv(StringIO(gas_csv), sep=";", decimal=".")
    gas = gas.dropna(subset=["€/kWh"])
    gas["Energie"] = "Gas"
    gas = gas.rename(columns={"Time period": "Zeit"})
    
    # Strom laden
    strom = pd.read_csv(StringIO(strom_csv), sep=";", decimal=".")
    strom = strom.dropna(subset=["Preis"])
    strom = strom.rename(columns={"Preis": "€/kWh", "Zeit": "Zeit"})
    strom["Energie"] = "Strom"
    
    # Zusammenführen
    df = pd.concat([gas, strom], ignore_index=True)
    df["Zeit"] = df["Zeit"].str.replace("-S", " H")
    return df

df = load_data()
countries = sorted(df["Geo"].unique())

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Preisverlauf pro Land",
    "2. Durchschnitt & Median",
    "3. Ausreißer-Analyse",
    "4. Boxplot Vergleich"
])

# Tab 1: Preisverlauf
with tab1:
    st.subheader("1. Preisverlauf Gas vs Strom pro Land")
    selected_country = st.selectbox("Land auswählen", countries, index=countries.index("Germany") if "Germany" in countries else 0, key="t1")
    df_land = df[df["Geo"] == selected_country]
    
    fig1 = px.line(
        df_land,
        x="Zeit",
        y="€/kWh",
        color="Energie",
        markers=True,
        title=f"Gas- und Strompreisentwicklung – {selected_country}",
        color_discrete_map={"Gas": "#1f77b4", "Strom": "#ff7f0e"},
        height=550
    )
    fig1.update_layout(xaxis_title="Zeitraum", yaxis_title="€/kWh", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

# Tab 2: Durchschnitt & Median
with tab2:
    st.subheader("2. Durchschnitt und Median pro Land")
    summary = df.groupby(["Geo", "Energie"])["€/kWh"].agg(Durchschnitt='mean', Median='median').reset_index()
    summary_melt = summary.melt(id_vars=["Geo", "Energie"], value_vars=["Durchschnitt", "Median"], var_name="Maß", value_name="€/kWh")
    
    fig2 = px.bar(
        summary_melt,
        x="Geo",
        y="€/kWh",
        color="Energie",
        barmode="group",
        facet_col="Maß",
        title="Durchschnitt und Median – Gas vs Strom",
        height=600,
        color_discrete_map={"Gas": "#1f77b4", "Strom": "#ff7f0e"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# Tab 3: Ausreißer
with tab3:
    st.subheader("3. Ausreißer-Analyse Gas vs Strom")
    st.markdown("""
    **Hinweis zur Ausreißer-Definition:**  
    Als mögliche Ausreißer gelten Werte mit einer Abweichung von **20–30 %**.  
    Ab **50 %** Abweichung handelt es sich fast immer um starke Ausreißer.  
    Die Abweichung wird vom **Mittelwert** des jeweiligen Energieträgers berechnet.
    """)
    
    selected_country_3 = st.selectbox("Land auswählen", countries, index=countries.index("Germany") if "Germany" in countries else 0, key="t3")
    threshold_pct = st.slider("Mindest-Abweichung vom Mittelwert", 5.0, 100.0, 20.0, 2.5, format="%.1f %%")
    
    df_c3 = df[df["Geo"] == selected_country_3].copy()
    for energie in ["Gas", "Strom"]:
        mask = df_c3["Energie"] == energie
        if mask.any():
            mean_val = df_c3.loc[mask, "€/kWh"].mean()
            df_c3.loc[mask, "Abweichung_%"] = ((df_c3.loc[mask, "€/kWh"] - mean_val) / mean_val * 100).round(1)
            df_c3.loc[mask, "Abs_Abweichung"] = df_c3.loc[mask, "Abweichung_%"].abs()
    
    # Weitere Logik kann hier ergänzt werden

# Tab 4: Boxplot
with tab4:
    st.subheader("4. Boxplot – Preisverteilung Gas vs Strom")
    fig4 = px.box(
        df,
        x="Geo",
        y="€/kWh",
        color="Energie",
        points="outliers",
        title="Vergleich der Preisverteilung: Gas vs Strom pro Land",
        height=650,
        color_discrete_map={"Gas": "#1f77b4", "Strom": "#ff7f0e"}
    )
    fig4.update_layout(xaxis_title="Land", yaxis_title="€/kWh", template="plotly_white")
    st.plotly_chart(fig4, use_container_width=True)

st.caption("Vergleich Gas- und Strompreise für Haushaltskunden 2020–2025 • Januar 2026")
