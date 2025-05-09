def tarjeta_style():
    return """
    <style>
        .custom-card {
            background-color: #2a4ba0;
            color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 
                0 2px 4px rgba(0, 0, 0, 0.25),
                0 4px 8px rgba(0, 0, 0, 0.15);
            margin: 15px 0;
            transition: all 0.3s ease;
            text-align: justify;
        }
        .custom-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }
        .card-title {
            margin-top: 0;
            text-align: center;
            color: #ffd700;
            font-family: 'Arial', sans-serif;
        }
        .card-content {
            line-height: 1.6;
        }
    </style>
    """