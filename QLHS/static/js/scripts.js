function loadClasses(obj) {
    fetch('/api/update', {
        method: 'put',
        body: JSON.stringify({
            'name': obj.value.slice(9, 11)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let lop = document.getElementById('lop-hoc')
        lop.innerHTML = ''
        for (let i = 0; i < data.size; i++) {
            lop.innerHTML += `
                <option>[${data.list[i+1].id}] ${data.list[i+1].name}</option>
            `
        }
    })
}


window.onload = function() {
    fetch ('/api/load-students', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let list = data.list
        let size = data.size

        let students = document.getElementById('students')

        for (let i = 0; i < size; i++) {
            students.innerHTML += `
                <option>[${list[i+1].id}] Tên HS: ${list[i+1].name}, Ngày sinh: ${list[i+1].day_of_birth}</option>
            `
        }
    })

    fetch('/api/update', {
        method: 'put',
        body: JSON.stringify({
            'name': '10'
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let lop = document.getElementById('lop-hoc')
        lop.innerHTML = ''
        for (let i = 0; i < data.size; i++) {
            lop.innerHTML += `
                <option>[${data.list[i+1].id}] ${data.list[i+1].name}</option>
            `
        }
    })
}

function addStudentToClass() {
    fetch('/api/add-student-to-class', {
        method: 'post',
        body: JSON.stringify({
            'student_id': parseInt(document.getElementById('students').value.slice(1,2)),
            'class_id': parseInt(document.getElementById('lop-hoc').value.slice(1,2))
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let msg = document.getElementById('msg')
        msg.innerHTML = data.msg
    })
}

function deleteStudent(student_id) {
    if (confirm('Hệ thống sẽ tiến hành xóa tất cả dữ liệu của học sinh này. Bạn có chắc chắn muốn xóa không') == true) {
        fetch('/api/delete-student/' + student_id, {
            method: 'delete',
            body: JSON.stringify({
                'student_id': student_id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            alert(data.msg)
            location.reload()
        })
    }
}

//function luuDiem(student_id, subject_id, id_hocKy) {
//    fetch('/api/nhap-diem', {
//        method: 'put',
//        body: JSON.stringify({
//            'student_id': parseInt(student_id),
//            'diem15Phut': document.getElementsClassName('diem15Phut').value,
//            'diem1Tiet': document.getElementsClassName('d1t').value,
//            'diemThi': document.getElementsClass('dt').value,
//            'subject_id': subject_id,
//            'id_hocKy': id_hocKy
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(res => res.json()).then(data => {
//        alert(data.msg)
//        location.reload()
//    })
//}


//function loadMark(subject_id, class_id, id_hocKy) {
//    fetch('/api/load-mark', {
//        method: 'post',
//        body: JSON.stringify({
//            'subject_id': parseInt(subject_id),
//            'class_id': parseInt(class_id),
//            'id_hocKy': parseInt(id_hocKy)
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(res => res.json()).then(data => {
////    document.getElementById('show-mark').innerHTML = ""
//        msg = document.getElementById('msg')
////        if (msg != '')
////            msg.innerHTML = data.msg
//        hk = document.getElementById('hk')
//        hk.innerHTML = "Học kỳ " + data.hocKy
//        show = document.getElementById('show-mark')
//        show.innerHTML = ''
//        list = data.list
//        for (let i = 0; i < data.size; i++) {
//            show.innerHTML += `
//                <tr>
//                    <td>${ data.list[i].stt }</td>
//                    <td>${ data.list[i].name }</td>
//                    <td>${ data.list[i].diem15Phut }</td>
//                    <td>${ data.list[i].diem1Tiet }</td>
//                    <td>${ data.list[i].diemThi }</td>
//                    <td>
//                        <a href="{{ url_for('nhap_diem', ?subject_id=${data.subject_id}, ?student_id=${data.list[i].student_id}, ?id_hocKy=${data.hocKy})}">Chỉnh sửa</a>
//                    </td>
//                </tr>
//            `
//        }
//    })
//}
