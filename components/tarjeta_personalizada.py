from styles.tarjetaStyle import tarjeta_style

def crear_tarjeta(title: str, content: str):
    tarjeta = tarjeta_style()
    
    return f"""
    {tarjeta}
    <div class="custom-card">
        <h3 class="card-title">{title}</h3>
        <p class="card-content">{content}</p>
    </div>
    """