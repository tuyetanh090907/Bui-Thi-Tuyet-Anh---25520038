from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register_students():
    try:
        # 1. Kiểm tra file có được gửi không
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "Không tìm thấy file JSON trong request."
            }), 400

        file = request.files["file"]

        # 2. Kiểm tra tên file
        if file.filename == "":
            return jsonify({
                "status": "error",
                "message": "Tên file không hợp lệ."
            }), 400

        if not file.filename.endswith(".json"):
            return jsonify({
                "status": "error",
                "message": "File phải có định dạng .json."
            }), 400

        # 3. Đọc nội dung file JSON
        data = json.load(file)

        if "students" not in data:
            return jsonify({
                "status": "error",
                "message": "Thiếu trường 'students' trong file JSON."
            }), 400

        students = data["students"]

        if not isinstance(students, list):
            return jsonify({
                "status": "error",
                "message": "'students' phải là một danh sách."
            }), 400

        total_students = len(students)
        seen_ids = set()
        duplicate_students = []
        unique_students = []

        # 4. Xử lý từng sinh viên
        for student in students:
            required_fields = ["student_id", "name", "age", "gender"]
            for field in required_fields:
                if field not in student:
                    return jsonify({
                        "status": "error",
                        "message": f"Thiếu trường bắt buộc: {field}"
                    }), 400

            if not isinstance(student["student_id"], str) \
               or not isinstance(student["name"], str) \
               or not isinstance(student["gender"], str):
                return jsonify({
                    "status": "error",
                    "message": "student_id, name, gender phải là chuỗi."
                }), 400

            if not isinstance(student["age"], int):
                return jsonify({
                    "status": "error",
                    "message": "age phải là số nguyên."
                }), 400

            student_id = student["student_id"]

            # Kiểm tra trùng
            if student_id in seen_ids:
                duplicate_students.append(student)
            else:
                seen_ids.add(student_id)
                unique_students.append(student)

        # 5. Lọc sinh viên đủ điều kiện (< 23 tuổi)
        eligible_students = [
            s for s in unique_students if s["age"] < 23
        ]

        # 6. Trả kết quả
        return jsonify({
            "status": "success",
            "message": "Danh sách đã được xử lý thành công.",
            "total_students": total_students,
            "duplicate_students": duplicate_students,
            "students_eligible_for_free_ticket": eligible_students
        }), 200

    except json.JSONDecodeError:
        return jsonify({
            "status": "error",
            "message": "File JSON không hợp lệ."
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Đã xảy ra lỗi trong quá trình xử lý.",
            "detail": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
