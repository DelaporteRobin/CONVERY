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

clockwork = Theme(
	name="clockwork",
	primary="#FF8436",
	secondary="#8902D6",
	background="#0f0e0d",
	surface="#0f0e0d",
	foreground="#ffffff",
	panel="#161414",
	warning="#D95D0F",
	success="#26C98A",
	error="#B51948",
	accent="#E8B94D",
	dark=True,
	)



theme_registry = [downtown_theme, abyss_theme, clockwork]