from textual.theme import Theme


downtown_theme = Theme(
	name="downtown",
	primary="#e41d59",
	secondary="#f76120",
	accent="#fd653d",
	foreground="#eacbd5",
	background="#29232e",
	success="#b7c664",
	warning="#cd854c",
	error="#cd5a4c",
	surface="#201b24",
	panel="#1a161d",
	dark=True,
	)

abyss_theme = Theme(
	name="abyss",
	primary="#8699da",
	secondary="#48b6bb",
	)

clockwork_dark = Theme(
	name="clockwork_dark",
	primary="#e15408",
	secondary="#bbaf99",
	background="#0f0e0d",
	surface="#0f0e0d",
	foreground="#ffffff",
	panel="#161414",
	warning="#ff9900",
	success="#59c337",
	error="#da4b12",
	dark=True,
	)

clockwork = Theme(
	name="clockwork",
	primary="#EB6036",
	secondary="#99B0BB",
	background="#222233",
	surface="#15151C",
	foreground="#ffffff",
	panel="#1A1A24",
	warning="#ff9900",
	success="#59c337",
	error="#da4b12",
	dark=True,
	)





theme_registry = [downtown_theme, abyss_theme, clockwork]