let searchType = 'room';
let lookData = null;

const searchSwitch = document.querySelectorAll('.search');
const searchAnswer = document.querySelector('#search-answer')
searchAnswer.focus();
for (let i = 0; i < searchSwitch.length; i++) {
    searchSwitch[i].addEventListener('click', (event) => {
        event.preventDefault();
        for (let i = 0; i < searchSwitch.length; i++) {
            searchSwitch[i].classList.remove('active');
        }
        console.log(event.target);
        event.target.classList.add('active');
        const activeSearch = document.querySelector('.active');
        searchType = activeSearch.id;
        console.log(searchType);
    });
}

searchAnswer.addEventListener('input', (event) => {
    console.log(event.target.value);
    let searchAnswer = event.target.value;
    fetch(`/api/search/${searchType}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            IDToken: localStorage.getItem('IDToken'),
            search: searchAnswer,
        })
    }).then(response => {
        return response.json();
    }
    ).then(data => {
        console.log(data);
        const loading = document.querySelector('#loading');
        if (data.length > 0) {
            loading.classList.add('hidden');
        } else {
            loading.classList.remove('hidden');
        }
        const searchResult = document.querySelector('#search-result');
        searchResult.innerHTML = '';
        for (let i = 0; i < data.length; i++) {
            const tr = document.createElement('tr');
            tr.classList.add('search-result', 'pb-2') // 'wow', 'animate__fadeInUp'
            tr.id = "data-" + data[i].id;
            searchResult.appendChild(tr);;
            const item = document.querySelector(`#data-${data[i].id}`);

            let td = document.createElement('td');
            td.classList.add('search-result-item', 'pb-2', 'w-2/6');
            td.innerHTML = data[i].room;
            item.appendChild(td);

            td = document.createElement('td');
            td.classList.add('search-result-item', 'pb-2', 'w-2/6');
            td.innerHTML = data[i].name;
            item.appendChild(td);

            td = document.createElement('td');
            td.classList.add('search-result-item', 'pb-2', 'w-2/6');
            let btn = document.createElement('button');
            btn.classList.add('lookData-btn', 'text-sm', 'font-medium', 'text-white', 'bg-blue-600', 'dark:bg-blue-500', 'p-1', 'rounded-lg');
            btn.innerHTML = "<i class='fas fa-search'></i><span class='ml-1'>查看</span>";
            btn.addEventListener('click', (event) => {
                const modalContainer = document.querySelector('#modal-container');
                modalContainer.classList.remove('out');
                modalContainer.classList.add("one");
                // const info_modal = document.querySelector('#info-form');
                const info_form = document.querySelector('#info-body');
                console.log(info_form);
                info_form.innerHTML = '';
                // info_modal.classList.remove("hidden");
                // info_modal.classList.add("flex");
                console.log(data[i].id);
                fetch('/api/info', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({
                        IDToken: localStorage.getItem('IDToken'),
                        id: data[i].id,
                    })
                }).then(response => {
                    return response.json();
                }
                ).then(data => {
                    console.log(data);
                    let img = "<img src='https://tipfile.takming.edu.tw/stuphoto/" + data.student_ID + ".jpg' class='w-20 h-auto rounded-lg' alt='TIP無此照片'>";
                    let title = ['照片', '國別', '房號', '床號', '班級', '學號', '姓名', '身分證字號', '生日', '手機', '家裡電話', '地址', '緊急聯絡人', '緊急聯絡人電話', '建立時間'];
                    let student = [img, data.country, data.room, data.bed, data.member_class, data.student_ID, data.name, data.ID_number, data.birthday, data.phone, data.home_phone, data.address, data.emergency_contact, data.emergency_contact_phone, data.created_at];
                    for (let i = 0; i < title.length; i++) {
                        let tr = document.createElement('tr');
                        tr.classList.add('px-4', 'pb-2');
                        info_form.appendChild(tr);
                        let td = document.createElement('td');
                        td.classList.add('info-form-item', 'pb-2');
                        td.innerHTML = title[i];
                        tr.appendChild(td);
                        td = document.createElement('td');
                        td.classList.add('info-form-item', 'pl-4', 'pb-2', 'flex', 'justify-center');
                        td.innerHTML = student[i];
                        tr.appendChild(td);
                    }
                }
                )

            });
            td.appendChild(btn);

            // td.innerHTML = "<button class='text-sm font-medium text-white bg-blue-600 dark:bg-blue-500 p-1 rounded-lg' id='lookData-btn' onclick='searchResultBtn(this)'><i class='fas fa-search'></i><span class='ml-1'>查看</span></button>";
            item.appendChild(td);
        }

    }
    )
});

const lookData_btn = document.querySelectorAll('.close-info-form');
for (let i = 0; i < lookData_btn.length; i++) {
    lookData_btn[i].addEventListener('click', (event) => {
        const modalContainer = document.querySelector('#modal-container');
        modalContainer.classList.add('out');
        // const info_modal = document.querySelector('#info-form');
        // info_modal.classList.add("hidden");
        // info_modal.classList.remove("flex");
    });
}