const loginForm = document.querySelector('#loginForm');
// const signUpForm = document.querySelector('#signUpForm');
const logoutBtn = document.querySelector('#logoutBtn');
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.16.0/firebase-auth.js";

loginForm.addEventListener('submit', (event) => {
    event.preventDefault();
    fetch('/api/login/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            username: loginForm.loginUsername.value,
        })
    }).then(response => {
        return response.json();
    }
    ).then(data => {
            const form = {
        email: data.email,
        password: loginForm.loginPassword.value,
    };
    console.log('[登入]', form);


    const auth = getAuth();
    signInWithEmailAndPassword(auth, form.email, form.password)
        .then(success => {
            success.user.getIdToken().then(idToken => {
                console.log('[登入成功]', idToken);
                fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify({ idToken }),
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('[登入成功]', data);
                        console.log('closeLoginForm');
                        const logincloseBtn = document.querySelector('#closeBtn');
                        logincloseBtn.classList.add('w-14');
                        console.log(logincloseBtn);
                        const loginSpan = document.querySelector('#login-span');
                        loginSpan.classList.add('hidden');
                        console.log(loginSpan);
                        const loginLoading = document.querySelector('#login-loading');
                        loginLoading.classList.remove('hidden');
                        loginLoading.classList.add('animate-spin');
                        setTimeout(() => {
                            closeLoginForm();
                        }, 3000);
                        window.location.reload();
                    });
            });
        })
        .catch(error => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log('[登入失敗]', errorCode, errorMessage);
            if (errorCode === 'auth/wrong-password') {
                alert('密碼錯誤');
            } else if (errorCode === 'auth/user-not-found') {
                alert('查無此帳號');
            } else {
                alert('登入失敗');
            }
        });
    })

});

// signUpForm.addEventListener('submit', (event) => {
//     event.preventDefault();
//     const form = {
//         email: signUpForm.signUpEmail.value,
//         password: signUpForm.signUpPassword.value,
//     };
//     console.log('[註冊]', form);
// });

if (logoutBtn !== null) {
    logoutBtn.addEventListener('click', (event) => {
        event.preventDefault();
        console.log('[登出]');
        fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log('[登出成功]', data);
                window.location.href = '/';
            })
        .catch(error => {
            console.log('[登出失敗]', error);
        });
    });
}