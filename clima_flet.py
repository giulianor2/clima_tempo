import flet as ft
import requests
import datetime
import pytz
import pycountry_convert as pc
from datetime import datetime


def main(page: ft.Page):
    page.title = "Previsão do Tempo"
    page.window.width = 600
    page.window.height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_400
    
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.icons.CLOUD), color='BLUE',
        leading_width=40,
        title=ft.Text('Clima e Tempo'),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.NOTIFICATIONS,
            ),
            ft.PopupMenuButton(
                items=[
                ft.PopupMenuItem(
                icon=ft.icons.PERSON,
                text='Perfil',
                    ),
                    ft.PopupMenuItem(
                        icon=ft.icons.SETTINGS,
                        text='Configurações',
                    ),
                ]
            ),
        ],
    )

    # Widgets
    local_input = ft.TextField(label="Cidade", width=300, color='black', bgcolor='grey')
    ver_clima_button = ft.ElevatedButton(
        text="Ver Clima",
        bgcolor='grey',
        color='black',
        on_click=lambda e: obter_clima(e, local_input.value),
        width=150,
    )
    
    cidade_label = ft.Text(size=20, weight=ft.FontWeight.BOLD, color='#1C1C1C')
    data_label = ft.Text(size=14, color='#1C1C1C')
    umidade_label = ft.Text(size=40, weight=ft.FontWeight.BOLD, color='#1C1C1C')
    umidade_simbolo_label = ft.Text(size=14, weight=ft.FontWeight.BOLD, color='#1C1C1C')
    umidade_nome_label = ft.Text(size=12, color='#1C1C1C')
    temp_label = ft.Text(size=30, weight=ft.FontWeight.BOLD, color='#1C1C1C')
    pressao_label = ft.Text(size=14, color='#1C1C1C')
    nivel_mar_label = ft.Text(size=14, color='#1C1C1C') 
    velocidade_label = ft.Text(size=14, color='#1C1C1C')
    descricao_label = ft.Text(size=14, color='#1C1C1C')
    icon_image = ft.Image()
    icon_image.src = "imagens/city.png"
    icon_image.width = 150
    icon_image.height = 150
    
    def obter_clima(e, cidade):
        weather_key = 'MY_API_KEY' #criar cadastro no site -> openweathermap.org
        api_link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={weather_key}&lang=pt"

        # Solicitação HTTP
        try:
            r = requests.get(api_link)
            data = r.json()
            print(data)

            # Processamento dos dados
            pais_codigo = data["sys"]["country"]
            zona_fuso = pytz.country_timezones[pais_codigo]
            pais = pytz.country_names[pais_codigo]
            zona = pytz.timezone(zona_fuso[0])
            zona_horas = datetime.now(zona).strftime("%d/%m/%Y | %H:%M:%S %p")
            temperatura = data["main"]["temp"]
            pressao = data["main"]["pressure"]
            nivel_mar = data["main"]["sea_level"]
            umidade = data["main"]["humidity"]
            velocidade = data["wind"]["speed"]
            descricao = data["weather"][0]["description"]

            temperatura_c = float(temperatura) - 273.15

            # Continente
            continente = pc.convert_continent_code_to_continent_name(
                pc.country_alpha2_to_continent_code(
                    pc.country_name_to_country_alpha2(pais)
                )
            )

            # Atualizando informações
            cidade_label.value = f"{cidade} - {pais} / {continente}"
            data_label.value = zona_horas
            umidade_label.value = f"{umidade}"
            umidade_simbolo_label.value = "%"
            umidade_nome_label.value = "Humidade"
            temp_label.value = f"Temperatura {temperatura_c:.2f}°C"
            pressao_label.value = f"Pressão: {pressao}"
            nivel_mar_label.value = f"Nível do Mar: {nivel_mar}"
            velocidade_label.value = f"Velocidade do vento: {velocidade}"
            descricao_label.value = descricao

            # Apresentando sol e lua
            zona_priodo = int(datetime.now(zona).strftime("%H"))
            if zona_priodo <= 5:
                icon_image.src = "imagens/lua.png"
                page.bgcolor = ft.colors.BLUE_GREY_200
            elif zona_priodo <= 11:
                icon_image.src = "imagens/sol_dia.png"
                page.bgcolor = ft.colors.LIGHT_BLUE
            elif zona_priodo <= 17:
                icon_image.src = "imagens/sol_tarde.png"
                page.bgcolor = ft.colors.YELLOW_100
            elif zona_priodo <= 23:
                icon_image.src = "imagens/lua.png"
                page.bgcolor = ft.colors.BLUE_GREY_200
            else:
                icon_image.src = "imagens/city.png"
                page.bgcolor = ft.colors.BLUE_GREY_200

            # Redesenhando a página
            page.update()

        except:
            ft.SnackBar(ft.Text("Cidade não encontrada!")).open = True
            page.update()

    # Layout da página
    page.add(
        app_bar,
        ft.Row(
            [
                local_input,
                ft.Container(width=10),
                ver_clima_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(height=20),
        ft.Row(
            [
                ft.Column(
                    [
                        cidade_label,
                        ft.Container(height=10),
                        data_label,
                        ft.Container(height=10),
                        ft.Row(
                            [
                                umidade_label,
                                umidade_simbolo_label,
                                umidade_nome_label
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        umidade_nome_label,
                        ft.Container(height=10),
                        temp_label,
                        pressao_label,
                        ft.Container(height=10),
                        nivel_mar_label,
                        ft.Container(height=10),
                        velocidade_label,
                        ft.Container(height=10),
                        descricao_label,
                    ]
                ),
                ft.Container(width=20),
                icon_image
            ]
        )
    )


ft.app(target=main)