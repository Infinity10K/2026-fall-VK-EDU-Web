function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const likeButtons = document.querySelectorAll('button[data-image-id]')

for (const item of likeButtons) {
    item.addEventListener('click', (e) => {
        const counter = document.querySelector(`span[data-like-counter="${item.dataset.imageId}"]`)
        counter.innerText = Number(counter.innerText) + 1

        const request = new Request(
            `/like_async/${item.dataset.imageId}/`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin' // Do not send CSRF token to another domain.
            }
        );
        fetch(request).then(function(response) {
            response.json().then((data) => {
                    counter.innerText = data.count
                }
            )

        });
    })
}
