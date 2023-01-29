const mobile_menu_1_btn = () => {
    const mobile_menu_1 = document.querySelector('#mobile-menu-1');
    mobile_menu_1.classList.toggle('hidden');
    mobile_menu_1.classList.toggle('block');
}

const mobile_menu_2_btn = () => {
    const mobile_menu_1 = document.querySelector('#mobile-menu-1');
    const mobile_menu_2 = document.querySelector('#mobile-menu-2');
    if (mobile_menu_1 !== null) {
        mobile_menu_1.classList.add('hidden');
    }
    mobile_menu_2.classList.toggle('hidden');
    mobile_menu_2.classList.toggle('block');
}

const loginBtn = document.querySelector('#loginBtn');
if (loginBtn !== null) {
    loginBtn.addEventListener('click', (event) => {
        console.log('loginBtn');
        event.preventDefault();
        const login_modal = document.querySelector('#login_modal');
        login_modal.classList.remove("opacity-0", "pointer-events-none");
    });
}

const closeLoginForm = () => {
    const login_modal = document.querySelector('#login_modal');
    login_modal.classList.add("opacity-0", "pointer-events-none");
}

// 黑暗模式
// let theme = localStorage.getItem('theme');
const dark_mode = () => {
    document.documentElement.classList.toggle('dark');
    if (document.documentElement.classList.contains('dark')) {
        localStorage.theme = 'dark';
    }
    else {
        localStorage.theme = 'light';
    }
    console.log(localStorage.theme);
}

let deleteID = null;
// const deleteBtn = document.querySelector('#deleteBtn');
const deleteBtn = document.querySelectorAll('.deleteBtn');
if (deleteBtn !== null) {
    for (let i = 0; i < deleteBtn.length; i++) {
        deleteBtn[i].addEventListener('click', (event) => {
            console.log('deleteBtn');
            event.preventDefault();
            const delete_modal = document.querySelector('#delete-form');
            delete_modal.classList.remove("hidden");
            delete_modal.classList.add("flex");
            deleteID = deleteBtn[i].id;
            console.log(deleteID);
        });
    }
}

const closeDeleteForm = document.querySelectorAll('.close-delete-form');
if (closeDeleteForm !== null) {
    for (let i = 0; i < closeDeleteForm.length; i++) {
        closeDeleteForm[i].addEventListener('click', (event) => {
            console.log('closeDeleteForm');
            event.preventDefault();
            const delete_modal = document.querySelector('#delete-form');
            delete_modal.classList.add("hidden");
            delete_modal.classList.remove("flex");
        });
    }
}

const deleteData = (id) => {
    console.log(id);
    fetch(`/api/delete/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    }).then(response => {
        return response.json();
    }
    ).then(data => {
        console.log(data);
        if (data.result === 'success') {
            window.location.reload()
        }
    }
    )
}


const card = document.querySelectorAll('.card');
if (card !== null) {
    for (let i = 0; i < card.length; i++) {
        card[i].addEventListener('mouseenter', (event) => {
            card[i].classList.add('active');

        });
        card[i].addEventListener('mouseleave', (event) => {
            card[i].classList.remove('active');
        }
        );
    }
}
