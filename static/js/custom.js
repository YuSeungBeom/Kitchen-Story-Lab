document.addEventListener('DOMContentLoaded', function() {
    // 기존 카드 호버 효과 유지
    
    // 좋아요 버튼 기능 개선
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            if (!document.querySelector('body').classList.contains('logged-in')) {
                window.location.href = '/accounts/login/';
                return;
            }

            try {
                const postId = this.dataset.postId;
                const response = await fetch(`/api/posts/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    this.classList.toggle('text-danger');
                    this.querySelector('.like-count').textContent = data.likes_count;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    // CSRF 토큰 가져오기 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});