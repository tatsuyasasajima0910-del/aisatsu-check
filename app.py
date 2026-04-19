import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='public', static_url_path='')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

STORE_MASTER = {
    'kannami': {
        'name': '関南店',
        'employees': [
            {'no': 2, 'name': '泉泰子'}, {'no': 3, 'name': '伊藤伝恵'},
            {'no': 11, 'name': '小坂亜弓'}, {'no': 16, 'name': '鈴木千明'},
            {'no': 28, 'name': '松本いずみ'}, {'no': 80, 'name': '松下龍'},
            {'no': 156, 'name': '金田美雪'}, {'no': 168, 'name': '大谷修'},
            {'no': 170, 'name': '古澤大輔'}, {'no': 193, 'name': '浦田琉聖'},
            {'no': 201, 'name': '吉村嘉恋'}, {'no': 220, 'name': '吉村嘉音'},
            {'no': 221, 'name': '野澤玲香'}, {'no': 226, 'name': '須田珠予'},
            {'no': 234, 'name': '柴田光江'},
        ]
    },
    'hanayama': {
        'name': '塙山店',
        'employees': [
            {'no': 83, 'name': '阿部奈津子'}, {'no': 84, 'name': '秋川麻衣子'},
            {'no': 88, 'name': '板倉博幸'}, {'no': 89, 'name': '小田部美香'},
            {'no': 98, 'name': '佐瀬敏之'}, {'no': 105, 'name': '根本裕子'},
            {'no': 108, 'name': '深沢環'}, {'no': 147, 'name': '小林柊太'},
            {'no': 181, 'name': '長久保颯生'}, {'no': 190, 'name': '生田目結太'},
            {'no': 200, 'name': '倉森啓汰'}, {'no': 203, 'name': '近藤瑠南'},
            {'no': 204, 'name': '㑹澤桃花'}, {'no': 205, 'name': '小室高世'},
            {'no': 212, 'name': '渡辺羚士'}, {'no': 217, 'name': '本間雅斗'},
            {'no': 218, 'name': '吉田翠'}, {'no': 225, 'name': '小室莉乃'},
            {'no': 232, 'name': '丹野久美子'}, {'no': 233, 'name': '荷見蒼葉'},
            {'no': 235, 'name': '小林沙樹'},
        ]
    },
    'shimosakurai': {
        'name': '下桜井店',
        'employees': [
            {'no': 9, 'name': '木村富江'}, {'no': 23, 'name': '飛田忍'},
            {'no': 24, 'name': '中野真寿美'}, {'no': 26, 'name': '松浦勝'},
            {'no': 33, 'name': '山下さゆり'}, {'no': 35, 'name': '渡邊恵美'},
            {'no': 124, 'name': '狩野雄祐'}, {'no': 129, 'name': 'タマンドングボズクアル'},
            {'no': 160, 'name': '伊藤佳央'}, {'no': 167, 'name': '小松笑美子'},
            {'no': 185, 'name': '大田和純愛'}, {'no': 207, 'name': '増井真弓'},
            {'no': 211, 'name': '竹澤乃咲'}, {'no': 224, 'name': '鈴木姫望'},
            {'no': 229, 'name': '和田麻衣'}, {'no': 231, 'name': '佐藤律輝'},
            {'no': 237, 'name': '鈴木佳代'}, {'no': 238, 'name': '安藤瑠良'},
            {'no': 239, 'name': '大和田瑠生'},
        ]
    }
}

def init_data():
    data = {}
    for key, store in STORE_MASTER.items():
        data[key] = {
            'meta': {'ofcName': '', 'checkPeriod': ''},
            'employees': [
                {
                    'no': emp['no'], 'name': emp['name'],
                    'aisatsu': '', 'koe': '', 'aisatsuDate': '', 'aisatsuMemo': '',
                    'osusume': '', 'reji': '', 'tennai': '', 'osusumeDate': '',
                    'osusumeMemo': '', 'updatedAt': ''
                }
                for emp in store['employees']
            ]
        }
    return data

def load_data():
    if not os.path.exists(DATA_FILE):
        data = init_data()
        save_data(data)
        return data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return init_data()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/store/<store_key>')
def get_store(store_key):
    data = load_data()
    if store_key not in data:
        return jsonify({'error': '店舗が見つかりません'}), 404
    return jsonify(data[store_key])

@app.route('/api/update', methods=['POST'])
def update_check():
    body = request.get_json()
    store_key = body.get('store')
    employee_no = body.get('employeeNo')
    fields = body.get('fields', {})

    data = load_data()
    if store_key not in data:
        return jsonify({'error': '店舗が見つかりません'}), 404

    emp = next((e for e in data[store_key]['employees'] if e['no'] == employee_no), None)
    if not emp:
        return jsonify({'error': '従業員が見つかりません'}), 404

    emp.update(fields)
    emp['updatedAt'] = datetime.now().isoformat()
    save_data(data)
    return jsonify({'ok': True})

@app.route('/api/meta', methods=['POST'])
def update_meta():
    body = request.get_json()
    store_key = body.get('store')
    data = load_data()
    if store_key not in data:
        return jsonify({'error': '店舗が見つかりません'}), 404
    data[store_key]['meta'] = {
        'ofcName': body.get('ofcName', ''),
        'checkPeriod': body.get('checkPeriod', '')
    }
    save_data(data)
    return jsonify({'ok': True})

@app.route('/api/dashboard')
def dashboard():
    data = load_data()
    result = {}
    for key, store in data.items():
        master = STORE_MASTER.get(key, {})
        emps = store['employees']
        n = len(emps)
        aisatsu_checked = sum(1 for e in emps if e.get('aisatsuDate'))
        result[key] = {
            'storeName': master.get('name', key),
            'total': n,
            'aisatsuChecked': aisatsu_checked,
            'aisatsuRate': round(aisatsu_checked / n * 100) if n > 0 else 0,
            'koeMaru2': sum(1 for e in emps if e.get('koe') == '◎'),
            'koeMaru1': sum(1 for e in emps if e.get('koe') == '〇'),
            'osusumeChecked': sum(1 for e in emps if e.get('osusumeDate')),
            'osusumeJisshi': sum(1 for e in emps if e.get('osusume') == '〇'),
            'reji': sum(1 for e in emps if e.get('reji') == '〇'),
            'tennai': sum(1 for e in emps if e.get('tennai') == '〇'),
            'ofcName': store['meta'].get('ofcName', ''),
            'checkPeriod': store['meta'].get('checkPeriod', ''),
        }
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
