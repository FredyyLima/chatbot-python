import qreader
import cv2

def extract_qrcode_data(image_path: str) -> str:
    try:
        # Carregar a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Imagem não encontrada ou inválida.")

        print(f"Dimensões da imagem: {image.shape}")

        # Converter para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aumentar o contraste
        _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # Decodificar o QR Code
        results = qreader.decodeQR(thresholded)

        # Verificar se algum QR Code foi encontrado
        if results:
            data = results[0].data.decode('utf-8')
            print(f"QR Code encontrado: {data}")
            return data
        else:
            print("Nenhum QR Code encontrado.")
            return "QR Code não encontrado."

    except Exception as e:
        print(f"Erro ao ler o QR Code: {e}")
        return f"Erro ao ler o QR Code: {e}"
