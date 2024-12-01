import hashlib
import os
import time
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'iiot_auth'
mysql = MySQL(app)


def hashing(data):
    # Hash data using SHA-256
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def xorope(value1, value2):
    # Perform XOR operation on two hex strings
    return hex(int(value1, 16) ^ int(value2, 16))[2:] 


def randomgen():
    # Generate a random hex string of 16 bytes
    return os.urandom(16).hex()


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        identity = data['identity']

        
        msk = randomgen()
        k = randomgen()
        T = randomgen()
        hashed_identity = hashing(identity)

        K_i = hashing(hashed_identity + k)
        X_i = hashing(msk + T)
        A_i = hashing(msk + K_i)
        B_i = xorope(K_i, X_i)
        alias_identity = xorope(hashed_identity, xorope(msk, K_i))

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO users (identity, alias_identity, A, B, T, msk)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (hashed_identity, alias_identity, A_i, B_i, T, msk)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'message': 'Registration successful',
            'alias_identity': alias_identity,
            'A_i': A_i,
            'B_i': B_i,
            'T': T
        })

    except Exception as e:
        return jsonify({'message': f'Registration failed. Error: {str(e)}'}), 500


@app.route('/generate_auth_request', methods=['POST'])
def generate_auth_request():
    try:
        data = request.json
        alias_identity = data.get('alias_identity', '')
        A_i = data.get('A_i', '')
        B_i = data.get('B_i', '')
        T = data.get('T', '')

        logger.debug(f"Received data: alias_identity={alias_identity}, A_i={A_i}, B_i={B_i}, T={T}")
        logger.info(f"Received data: alias_identity={alias_identity}, A_i={A_i}, B_i={B_i}, T={T}")

        if not all([alias_identity, A_i, B_i, T]):
            logger.error("Invalid input: Missing required fields.")
            return jsonify({'message': 'Invalid input: Missing required fields'}), 400

        cursor = mysql.connection.cursor()
        logger.debug("Executing SQL Query to fetch msk.")
        cursor.execute("SELECT msk FROM users WHERE T = %s", (T,))
        user_data = cursor.fetchone()
        cursor.close()

        if not user_data:
            logger.error("Invalid T value or user not found.")
            return jsonify({'message': 'Invalid T value or user not found'}), 404

        msk = user_data[0]
        
        ri = randomgen()
        
        Ri = hashing(ri)

        X_i = hashing(msk + T)

        K_i = xorope(B_i, X_i)
        
        aidi = xorope(alias_identity, xorope(msk, K_i))
        
        idi = xorope(aidi, xorope(msk, K_i))
        

        m1 = xorope(ri, A_i)
        m2 = xorope(aidi, Ri)
        ti = str(int(time.time()))
        m3 = hashing(idi + ri + A_i + T + ti)

        

        return jsonify({
            'm1': m1,
            'm2': m2,
            'm3': m3,
            'ti': ti,
            'B_i': B_i,
            'T': T
        })

    except Exception as e:
        logger.error(f"Error generating authentication request: {str(e)}", exc_info=True)
        return jsonify({'message': f'Error generating authentication request: {str(e)}'}), 500



@app.route('/verify_authentication', methods=['POST'])
def verify_authentication():
    try:
        data = request.json
        ti = data['ti']
        m1 = data['m1']
        m2 = data['m2']
        m3 = data['m3']
        B_i = data['B_i']
        T = data['T']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT msk FROM users WHERE T = %s", (T,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return jsonify({'message': 'Authentication failed. Invalid T.'}), 401

        msk = result[0]
        X_i = hashing(msk + T)
        K_i = xorope(B_i, X_i)
        A_i = hashing(msk + K_i)
        ri = xorope(m1, A_i)
        Ri = hashing(ri)
        aidi = xorope(m2, Ri)
        idi = xorope(aidi, xorope(msk, K_i))
        m3_prime = hashing(idi + ri + A_i + T + ti)
        
        logger.info(f"Verification Values: idi={idi}, ri={ri}, A_i={A_i}, T={T}, ti={ti}, m3_prime={m3_prime}")


        if m3_prime == m3:
            return jsonify({'message': 'Authentication successful m3==m3` request by user verified.'}), 200
        else:
            return jsonify({'message': 'Authentication failed. Invalid m3.'}), 401

    except Exception as e:
        return jsonify({'message': f'Authentication failed. Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)