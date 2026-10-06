from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# 前端網頁 HTML 範本
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BMI 計算器</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .container { max-width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; }
        input { width: 90%; padding: 8px; margin: 10px 0; }
        button { width: 95%; padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
        #result { margin-top: 20px; font-weight: bold; font-size: 1.2em; color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h2>BMI 計算器</h2>
        <input type="number" id="height" placeholder="身高 (公分)" step="0.1">
        <input type="number" id="weight" placeholder="體重 (公斤)" step="0.1">
        <button onclick="calculateBMI()">計算 BMI</button>
        <div id="result"></div>
    </div>

    <script>
        function calculateBMI() {
            const height = document.getElementById('height').value;
            const weight = document.getElementById('weight').value;
            
            if(!height || !weight) {
                document.getElementById('result').innerText = "請輸入完整身高與體重！";
                return;
            }

            fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ height: parseFloat(height), weight: parseFloat(weight) })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('result').innerHTML = `BMI 指數: ${data.bmi}<br>評語: ${data.status}`;
            })
            .catch(() => {
                document.getElementById('result').innerText = "連線發生錯誤";
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    height = data.get('height') / 100  # 公分轉公尺
    weight = data.get('weight')
    
    # 計算 BMI
    bmi = round(weight / (height ** 2), 2)
    
    # 判斷狀態
    if bmi < 18.5:
        status = "體重過輕"
    elif bmi < 24:
        status = "健康體重"
    else:
        status = "體重過重"
        
    return jsonify({'bmi': bmi, 'status': status})

if __name__ == '__main__':
    # Render 規定必須綁定 0.0.0.0 並讀取環境變數的 PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
