document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("mainNavbar");
    const originalClasses = ["w-75", "rounded-pill", "py-3"];
    const newClasses = ["w-100", "py-4"];
    let isScrolled = false;

    function navAnimation(){
        if (window.scrollY > 75 && !isScrolled) {
            originalClasses.forEach(cls => navbar.classList.remove(cls));
            navbar.style.top = 0;
            newClasses.forEach(cls => navbar.classList.add(cls));
            isScrolled = true;
        } else if (window.scrollY <= 75 && isScrolled) {
            originalClasses.forEach(cls => navbar.classList.add(cls));
            navbar.style.top = "1.5%";
            newClasses.forEach(cls => navbar.classList.remove(cls));
            isScrolled = false;
        }
    }
    
    window.addEventListener("scroll", navAnimation);
    window.addEventListener('load', navAnimation);

    const elements = document.querySelectorAll(".fadeIn, .slideInUp, .zoomIn, .fadeInUp, .fadeInDown, .fadeInLeft, .fadeInRight, .flipInX");

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;

            el.classList.add("visible");

            if (el.classList.contains('zoomIn')) {
                el.classList.remove('zoomIn');
                el.classList.add('animate__animated', 'animate__zoomIn');
            }

            if (el.classList.contains('slideInUp')) {
                el.classList.remove('slideInUp');
                el.classList.add('animate__animated', 'animate__slideInUp');
            }

            if (el.classList.contains('fadeIn')) {
                el.classList.remove('fadeIn');
                el.classList.add('animate__animated', 'animate__fadeIn');
            }

            if (el.classList.contains('fadeInUp')) {
                el.classList.remove('fadeInUp');
                el.classList.add('animate__animated', 'animate__fadeInUp');
            }

            if (el.classList.contains('fadeInDown')) {
                el.classList.remove('fadeInDown');
                el.classList.add('animate__animated', 'animate__fadeInDown');
            }

            if (el.classList.contains('fadeInLeft')) {
                el.classList.remove('fadeInLeft');
                el.classList.add('animate__animated', 'animate__fadeInLeft');
            }

            if (el.classList.contains('fadeInRight')) {
                el.classList.remove('fadeInRight');
                el.classList.add('animate__animated', 'animate__fadeInRight');
            }

            if (el.classList.contains('flipInX')) {
                el.classList.remove('flipInX');
                el.classList.add('animate__animated', 'animate__flipInX');
            }

            observer.unobserve(el); 
        }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => observer.observe(el));
    elements.forEach(el => {
        el.addEventListener('animationend', () => {
            el.classList.remove('animate__animated');
        });
    });

    const toggleButton = document.getElementById('catalogToggle');
    const catalogToggleMobile = document.getElementById('catalogToggleMobile');
    const categoryPanel = document.getElementById('categoryPanel');
    const catalogToggleFooter = document.getElementById('catalogToggleFooter');

    categoryPanel.addEventListener('animationend', () => {
        if (categoryPanel.classList.contains('animate__fadeOutUp')) {
            categoryPanel.classList.add('d-none');
        }
    });


    [toggleButton, catalogToggleMobile, catalogToggleFooter].forEach(toogle => {
        toogle.addEventListener('click', () => {
            if (categoryPanel.classList.contains('animate__fadeOutUp') || categoryPanel.classList.contains('d-none')) {
            categoryPanel.classList.remove('animate__fadeOutUp');
            categoryPanel.classList.remove('d-none');
            categoryPanel.classList.add('animate__fadeInDown');
            } else {
            categoryPanel.classList.remove('animate__fadeInDown');
            categoryPanel.classList.add('animate__fadeOutUp');
            }
        });
    });

    // Закрытие при клике вне
    document.addEventListener('click', (e) => {
        if (!categoryPanel.contains(e.target) && !toggleButton.contains(e.target) && !catalogToggleMobile.contains(e.target) && !catalogToggleFooter.contains(e.target)) {
            categoryPanel.classList.add('d-none');
            categoryPanel.classList.remove('animate__fadeInDown');
        }
    });

    const categoryEl = document.querySelectorAll('.category-el');
    const SubcategoryPlace = document.getElementById('SubcategoryPlace');
    categoryEl.forEach(el => {
        el.addEventListener('mouseenter', () => {
            SubcategoryPlace.innerHTML = el.querySelector('.subcategory-container').innerHTML;
            const elementsCategories = SubcategoryPlace.querySelectorAll('.list-group-item.list-group-item-action');
            elementsCategories.forEach((elem, index) => {
                elem.classList.add('animate__animated', 'animate__zoomIn');
                elem.style.setProperty('animation-delay', `${index * 0.1}s`);
                elem.style.setProperty('animation-duration', '0.5s');

                elem.addEventListener('animationend', ()=> {
                    elem.classList.remove('animate__animated', 'animate__zoomIn');
                }, {once: true});
            });
            categoryEl.forEach(el => {
                el.classList.remove('active');
            });
            el.classList.add('active');
        });
    });

    function addMessageChat(message, sender, created_at, id) {
        const isSupport = sender === 'support';

        const messageClass = isSupport
            ? 'bg-light'
            : 'bg-orange text-white align-self-end';

        const messagesContainer = document.getElementById('messagesContainer');
        if (!messagesContainer) return;

        const div = document.createElement('div');
        div.className = `w-fit-content rounded-custom p-2 px-3 list-group-item border shadow-sm ${messageClass} animate__animated animate__zoomIn`;

        const key = `${created_at}_${id}`;
        div.setAttribute('data-key', key);

        const messageText = document.createElement('div');
        messageText.textContent = message;

        const timeWrapper = document.createElement('div');
        timeWrapper.className = isSupport ? 'text-start' : 'text-end';

        const timeText = document.createElement('small');
        timeText.className = isSupport ? 'text-muted' : 'text-white';
        timeText.style.fontSize = 'small';

        let timeOnly;
        if(created_at){
            timeOnly = new Date(created_at).toLocaleTimeString('uk-UA', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            });
        } else {
            const now = new Date();
            const hours = now.getHours(); 
            const minutes = now.getMinutes(); 

            timeOnly = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
        }

        timeText.textContent = timeOnly;
        timeWrapper.appendChild(timeText);

        div.appendChild(messageText);
        div.appendChild(timeWrapper);

        div.addEventListener('animationend', () => {
            div.classList.remove('animate__animated', 'animate__zoomIn');
        }, { once: true });

        messagesContainer.appendChild(div);
        UpdatedisplayedMessagesList();
    }

    const button = document.getElementById('PhoneButton');
    const PhoneBadge = document.getElementById('PhoneBadge');
    const ChatWrapper = document.getElementById('ChatWrapper');
    const ChatClose = document.querySelector('#ChatWrapper .btn-close.btn-close-white');

    let pollIntervalId = null;

    const displayedMessages = new Set();
    UpdatedisplayedMessagesList();

    function UpdatedisplayedMessagesList() {
        document.querySelectorAll('#messagesContainer [data-key]').forEach(el => {
            if (!displayedMessages.has(el.dataset.key)) {
                displayedMessages.add(el.dataset.key);
            }
        });
    }

    async function fetchChatUpdates() {
        if (!ChatWrapper.classList.contains('animate-zoomInFromCircle')) return;

        try {
            const res = await fetch('/chat/upload-chat/');
            if (!res.ok) throw new Error(res.status);
            const data = await res.json();

            for (const msg of data.messages) {
                const key = `${msg.created_at}_${msg.id}`;

                if (displayedMessages.has(key)) continue;

                addMessageChat(msg.message, msg.role, msg.created_at, msg.id);
                displayedMessages.add(key);
            }

        } catch (e) {
            console.error('Ошибка polling:', e);
        }
    }

    function startPolling() {
        if (pollIntervalId) return;
        fetchChatUpdates();
        pollIntervalId = setInterval(fetchChatUpdates, 60_000);
    }

    function stopPolling() {
        if (!pollIntervalId) return;
        clearInterval(pollIntervalId);
        pollIntervalId = null;
    }
    
    button.addEventListener('mouseenter', () => {
        PhoneBadge.classList.remove('animate-zoomRightOut');
        PhoneBadge.classList.add('animate-zoomRightIn');
    });

    button.addEventListener('mouseleave', () => {
        PhoneBadge.classList.remove('animate-zoomRightIn');
        PhoneBadge.classList.add('animate-zoomRightOut');
    });

    let botMessageShown = false;

    button.addEventListener('click', () => {
        UpdatedisplayedMessagesList();
        button.classList.add('d-none');
        ChatWrapper.classList.remove('animate-zoomOutToCircle');
        ChatWrapper.classList.add('animate-zoomInFromCircle');

        if (!botMessageShown) {
            botMessageShown = true;

            const typingContainer = document.querySelector('.typing-indicator-container');
                
            setTimeout(() => {
                if (typingContainer) {
                    typingContainer.remove();
                    addMessageChat("Вітаю! Чим можу допомогти?", "support");
                } 
            }, 2000);
        }
        startPolling();
    });

    const form = document.getElementById('SendMessageForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const messageInput = form.querySelector('input[name="message"]');
        const message = messageInput.value.trim();
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

        if (!message) return;

        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ message: message })
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сервера');
            return response.json();
        })
        .then(data => {
            messageInput.value = '';

            addMessageChat(data.message, 'user', data.message_time, data.message_id); 
        })
        .catch(error => {
            console.error('Ошибка при отправке сообщения:', error);
        });
    });

    ChatClose.addEventListener('click', () => {
        ChatWrapper.classList.remove('animate-zoomInFromCircle');
        ChatWrapper.classList.add('animate-zoomOutToCircle');
        stopPolling();
    });

    ChatWrapper.addEventListener('animationend', () => {
        if (ChatWrapper.classList.contains('animate-zoomOutToCircle')) {
            button.classList.remove('d-none');
        }
    });

    const pulseTargetElemOnclick = document.querySelectorAll('.pulseTargetElemOnclick');

    pulseTargetElemOnclick.forEach(elem => {
        elem.addEventListener('click', () => {
            EasyToSeeElement(elem.href.substring(elem.href.indexOf('#') + 1));
        });
    });

    function EasyToSeeElement(element){
        element = document.getElementById(element);
        if (element) {
            element.classList.add("pulse-highlight");

            setTimeout(() => element.classList.remove("pulse-highlight"), 4000);
        }
    }

    const deleteForms = document.querySelectorAll('.delete-form');
    const csrfField = document.querySelector('[name="csrfmiddlewaretoken"]');
    const token = csrfField.value;

    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            e.stopPropagation();

            const formData = new FormData(e.target);
            const url = e.target.getAttribute('action');
            
            PostFormRequest(url, formData, e.target);
        });
    });

    function showToast(message, color = '#28a745') {
        const container = document.getElementById('toastContainer');
        if (!container) {
            console.error('Toast container not found!');
            return;
        }

        const toastEl = document.createElement('div');
        toastEl.className = 'toast show rounded-custom overflow-hidden p-1 px-2 mb-2';
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        toastEl.style.zIndex = '9999';
        toastEl.style.top = '20px';
        toastEl.style.left = '20px';

        toastEl.innerHTML = `
            <div class="toast-header px-3 py-2">
                <span class="rounded-circle me-2" style="width: 10px; height: 10px; background-color: ${color};"></span>
                <img src="/static/images/logo.png" height="20" width="20" class="rounded me-2" alt="PFB Typography">
                <strong class="me-auto">PFB Typography</strong>
                <small class="text-body-secondary">Зараз</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        container.prepend(toastEl);

        const toast = new bootstrap.Toast(toastEl, { autohide: false });
        toast.show();
    }

    function PostFormRequest(url, formData, formElement) {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': token,
            },
            body: formData,
        })
        .then(response => {
            return response.json().then(data => {
                if (!response.ok) {
                    showToast(data.error || 'Сталася помилка.', '#dc3545');
                    console.error("Помилка запиту:", response.status);
                } else {
                    showToast(data.message || 'Операція виконана успішно.', '#28a745');
                    
                    const itemCard = formElement.closest('.card.mb-1');
                    if (itemCard) {
                        itemCard.remove();
                    }
                    
                    updateTotalPrice(data.new_total_price);
                    
                    const itemsContainer = document.querySelector('#cartModal .modal-body .row.row-cols-1.g-3 > .col');
                    const remainingItems = itemsContainer ? itemsContainer.querySelectorAll('.card.mb-1').length : 0;

                    if (remainingItems === 0) {
                        const mainCard = document.querySelector('#cartModal .modal-body .row.row-cols-1.g-3');
                        if (mainCard) {
                            mainCard.remove();
                        }

                        const modalBody = document.querySelector('#cartModal .modal-body');
                        if (modalBody) {
                            modalBody.innerHTML = 'У вас поки немає замовлень.';
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error("Помилка мережі:", error);
            showToast('Помилка мережі. Спробуйте ще раз.', '#dc3545');
        });
    }

    function updateTotalPrice(newPrice) {
        const totalPriceBadge = document.querySelector('#cartModal .badge.bg-orange');
        if (totalPriceBadge) {
            totalPriceBadge.textContent = `${parseFloat(newPrice).toFixed(2)} грн`;
        }
    }
});