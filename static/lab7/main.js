// main.js - для дополнительного задания с базой данных
// Функция для заполнения таблицы фильмами из базы данных
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            // Получаем тело таблицы по id и очищаем его
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            if (films.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="4" style="padding: 20px; text-align: center; color: #666;">
                            Нет фильмов в базе данных. Добавьте первый фильм!
                        </td>
                    </tr>
                `;
                return;
            }
            
            // Пробегаемся по массиву фильмов
            for(let i = 0; i < films.length; i++) {
                let film = films[i];
                // Создаем строку
                let tr = document.createElement('tr');
                
                // Создаем ячейки
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                
                // Заполняем данными
                tdTitle.innerHTML = film.title === film.title_ru ? 
                    '<span style="color: #666; font-style: italic;">(то же что и русское)</span>' : 
                    film.title;
                tdTitleRus.innerHTML = film.title_ru;
                tdYear.innerHTML = film.year;
                
                // Создаем кнопки
                let editButton = document.createElement('button');
                editButton.innerHTML = 'редактировать';
                editButton.className = 'btn btn-edit';
                editButton.onclick = function() {
                    loadFilmForEdit(film.id);
                };
                
                let delButton = document.createElement('button');
                delButton.innerHTML = 'удалить';
                delButton.className = 'btn btn-delete';
                delButton.onclick = function() {
                    deleteFilm(film.id, film.title_ru);
                };
                
                // Добавляем кнопки в ячейку действий
                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);
                
                // Добавляем ячейки в строку
                tr.appendChild(tdTitle);
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);
                
                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            }
            
            // Обновляем статистику
            updateStats();
        })
        .catch(function (error) {
            console.error('Ошибка загрузки фильмов из базы данных:', error);
            document.getElementById('film-list').innerHTML = 
                '<tr><td colspan="4" style="color: red; text-align: center; padding: 20px;">Ошибка загрузки данных из базы данных. Проверьте подключение.</td></tr>';
        });
}

// Функция загрузки фильма для редактирования
function loadFilmForEdit(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Фильм не найден в базе данных');
            }
            return response.json();
        })
        .then(function(film) {
            // Заполняем форму редактирования
            document.getElementById('editId').value = id;
            document.getElementById('editTitle').value = film.title;
            document.getElementById('editTitleRu').value = film.title_ru;
            document.getElementById('editYear').value = film.year;
            document.getElementById('editDescription').value = film.description;
            
            // Показываем сообщение
            const output = document.getElementById('output');
            output.innerHTML = `<div class="success-message">
                <h3>Редактирование фильма #${id} из базы данных</h3>
                <p><strong>Название:</strong> "${film.title_ru}"</p>
                <p>Заполните форму выше и нажмите "Обновить фильм в БД"</p>
            </div>`;
            
            // Очищаем ошибки
            clearEditFormErrors();
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            const output = document.getElementById('output');
            output.innerHTML = `<div class="error-box">
                <h3>Ошибка загрузки из базы данных</h3>
                <p>${error.message}</p>
            </div>`;
        });
}

// Функция удаления фильма из базы данных
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}" из базы данных?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function(response) {
        const output = document.getElementById('output');
        if (response.status === 204) {
            output.innerHTML = `<div class="success-message">
                <h3>Фильм "${title}" успешно удален из базы данных!</h3>
                <p>ID: ${id} больше не существует в таблице lab7_movies</p>
            </div>`;
            
            // Перезагружаем таблицу
            setTimeout(fillFilmList, 500);
        } else {
            response.json().then(function(error) {
                output.innerHTML = `<div class="error-box">
                    <h3>Ошибка при удалении из базы данных</h3>
                    <p>${error.error || 'Неизвестная ошибка базы данных'}</p>
                </div>`;
            });
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        const output = document.getElementById('output');
        output.innerHTML = `<div class="error-box">
            <h3>Ошибка соединения с базой данных</h3>
            <p>Проверьте подключение к серверу и базу данных</p>
        </div>`;
    });
}

// Функция для показа формы добавления
function addFilm() {
    const output = document.getElementById('output');
    const currentYear = new Date().getFullYear();
    
    output.innerHTML = `
        <div class="card">
            <h3>Добавление нового фильма в базу данных</h3>
            <div class="form-group">
                <label class="form-label">Название на русском: <span style="color: #f44336;">*</span></label>
                <input type="text" id="newTitleRu" class="form-control" placeholder="Введите русское название">
                <div class="note">Обязательное поле (валидация на бэкенде)</div>
            </div>
            <div class="form-group">
                <label class="form-label">Оригинальное название:</label>
                <input type="text" id="newTitle" class="form-control" placeholder="Введите оригинальное название">
                <div class="note">Если оставить пустым, будет использовано русское название</div>
            </div>
            <div class="form-group">
                <label class="form-label">Год выпуска: <span style="color: #f44336;">*</span></label>
                <input type="number" id="newYear" min="1895" max="${currentYear}" value="${currentYear}" 
                       class="form-control" placeholder="Год выпуска" style="width: 150px;">
                <div class="note">Диапазон: 1895-${currentYear} (валидация на бэкенде)</div>
            </div>
            <div class="form-group">
                <label class="form-label">Описание: <span style="color: #f44336;">*</span></label>
                <textarea id="newDescription" rows="4" class="form-control" 
                          placeholder="Введите описание фильма (максимум 2000 символов)"></textarea>
                <div class="note">Обязательное поле, максимум 2000 символов (валидация на бэкенде)</div>
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="submitNewFilm()" class="btn btn-primary">
                    Добавить фильм в БД
                </button>
                <button onclick="fillFilmList()" class="btn btn-secondary">
                    Отмена
                </button>
            </div>
            <p class="note" style="margin-top: 15px;">
                <span style="color: #f44336;">*</span> - обязательные поля с валидацией на бэкенде
            </p>
        </div>
    `;
}

// Функция добавления нового фильма в базу данных
function submitNewFilm() {
    const title = document.getElementById('newTitle').value;
    const titleRu = document.getElementById('newTitleRu').value;
    const year = document.getElementById('newYear').value;
    const description = document.getElementById('newDescription').value;
    const currentYear = new Date().getFullYear();
    
    // Очищаем ошибки
    clearErrorMessages();
    
    // Простая валидация на клиенте
    let hasError = false;
    
    if (!titleRu.trim()) {
        showError('newTitleRu', 'Русское название обязательно');
        hasError = true;
    }
    
    if (!year || year < 1895 || year > currentYear) {
        showError('newYear', `Год должен быть в диапазоне 1895-${currentYear}`);
        hasError = true;
    }
    
    if (!description.trim()) {
        showError('newDescription', 'Описание обязательно');
        hasError = true;
    } else if (description.length > 2000) {
        showError('newDescription', 'Описание не должно превышать 2000 символов');
        hasError = true;
    }
    
    if (hasError) {
        const output = document.getElementById('output');
        output.innerHTML = `<div class="error-box">
            <h3>Исправьте ошибки в форме перед отправкой в базу данных</h3>
            <p>Клиентская валидация не прошла</p>
        </div>`;
        return;
    }
    
    const filmData = {
        title: title.trim(),
        title_ru: titleRu.trim(),
        year: parseInt(year),
        description: description.trim()
    };
    
    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filmData)
    })
    .then(function(response) {
        if (response.status === 201) {
            return response.json();
        } else if (response.status === 400) {
            return response.json().then(errorData => {
                showBackendErrors(errorData, 'new');
                throw new Error('Ошибка валидации на бэкенде');
            });
        } else {
            throw new Error('Ошибка добавления фильма в базу данных');
        }
    })
    .then(function(result) {
        const output = document.getElementById('output');
        output.innerHTML = `<div class="success-message">
            <h3>Новый фильм успешно добавлен в базу данных!</h3>
            <p>ID нового фильма в таблице lab7_movies: <strong>${result.id}</strong></p>
            <p><strong>Данные записаны в SQLite базу данных:</strong></p>
            <pre>${JSON.stringify(filmData, null, 2)}</pre>
        </div>`;
        
        // Обновляем таблицу
        fillFilmList();
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        if (error.message !== 'Ошибка валидации на бэкенде') {
            const output = document.getElementById('output');
            output.innerHTML = `<div class="error-box">
                <h3>Ошибка при добавлении в базу данных</h3>
                <p>${error.message}</p>
            </div>`;
        }
    });
}

// Функция для отправки формы редактирования
window.editFilmSubmit = async function() {
    const id = document.getElementById('editId').value;
    const title = document.getElementById('editTitle').value;
    const titleRu = document.getElementById('editTitleRu').value;
    const year = document.getElementById('editYear').value;
    const description = document.getElementById('editDescription').value;
    const currentYear = new Date().getFullYear();
    
    // Очищаем ошибки
    clearErrorMessages();
    
    // Валидация на клиенте
    let hasError = false;
    
    if (!titleRu.trim()) {
        showError('editTitleRu', 'Русское название обязательно');
        hasError = true;
    }
    
    if (!year || year < 1895 || year > currentYear) {
        showError('editYear', `Год должен быть в диапазоне 1895-${currentYear}`);
        hasError = true;
    }
    
    if (!description.trim()) {
        showError('editDescription', 'Описание обязательно');
        hasError = true;
    } else if (description.length > 2000) {
        showError('editDescription', 'Описание не должно превышать 2000 символов');
        hasError = true;
    }
    
    if (hasError) {
        const output = document.getElementById('output');
        output.innerHTML = `<div class="error-box">
            <h3>Исправьте ошибки в форме</h3>
            <p>Клиентская валидация не прошла</p>
        </div>`;
        return;
    }
    
    const filmData = {
        title: title.trim(),
        title_ru: titleRu.trim(),
        year: parseInt(year),
        description: description.trim()
    };
    
    try {
        const response = await fetch(`/lab7/rest-api/films/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filmData)
        });
        
        const output = document.getElementById('output');
        
        if (response.status === 200) {
            const updatedFilm = await response.json();
            output.innerHTML = `<div class="success-message">
                <h3>Фильм #${id} успешно обновлен в базе данных!</h3>
                <p><strong>Обновленные данные в таблице lab7_movies:</strong></p>
                <pre>${JSON.stringify(updatedFilm, null, 2)}</pre>
            </div>`;
            
            // Обновляем таблицу
            fillFilmList();
        } else if (response.status === 400) {
            const errorData = await response.json();
            showBackendErrors(errorData, 'edit');
        } else {
            const error = await response.json();
            output.innerHTML = `<div class="error-box">
                <h3>Ошибка обновления в базе данных</h3>
                <pre>${JSON.stringify(error, null, 2)}</pre>
            </div>`;
        }
    } catch (error) {
        console.error('Ошибка:', error);
        const output = document.getElementById('output');
        output.innerHTML = `<div class="error-box">
            <h3>Ошибка соединения с базой данных</h3>
            <p>${error.message}</p>
        </div>`;
    }
};

// Функция обновления статистики
function updateStats() {
    fetch('/lab7/rest-api/films/')
        .then(r => r.json())
        .then(films => {
            document.getElementById('films-count').textContent = films.length;
            
            // Находим максимальный ID
            const maxId = films.length > 0 ? Math.max(...films.map(f => f.id)) : 0;
            document.getElementById('max-id').textContent = maxId;
        });
}

// Вспомогательные функции для работы с ошибками
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    // Удаляем старую ошибку если есть
    const oldError = field.parentNode.querySelector('.error-message');
    if (oldError) {
        oldError.remove();
    }
    
    field.parentNode.appendChild(errorDiv);
    field.classList.add('error-field');
}

function clearErrorMessages() {
    // Очищаем все сообщения об ошибках
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Сбрасываем стили полей
    document.querySelectorAll('.error-field').forEach(el => {
        el.classList.remove('error-field');
    });
}

function clearEditFormErrors() {
    const fields = ['editTitle', 'editTitleRu', 'editYear', 'editDescription'];
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.classList.remove('error-field');
            const errorMsg = field.parentNode.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        }
    });
}

function showBackendErrors(errorData, formPrefix = '') {
    const output = document.getElementById('output');
    
    if (errorData.errors && Array.isArray(errorData.errors)) {
        let html = `<div class="error-box"><h3>Ошибки валидации на бэкенде:</h3><ul>`;
        errorData.errors.forEach(error => {
            html += `<li><strong>${error.field}:</strong> ${error.message}</li>`;
            
            // Подсвечиваем поле с ошибкой
            const fieldId = formPrefix ? formPrefix + capitalizeFirstLetter(error.field) : error.field;
            const field = document.getElementById(fieldId);
            if (field) {
                field.classList.add('error-field');
            }
        });
        html += `</ul><p>Исправьте ошибки и попробуйте снова.</p></div>`;
        output.innerHTML = html;
    } else if (errorData.error) {
        output.innerHTML = `<div class="error-box">
            <h3>Ошибка базы данных:</h3>
            <p>${errorData.error}</p>
        </div>`;
    }
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Автоматически загружаем фильмы при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
    
    // Очистка ошибок при фокусе
    document.addEventListener('focusin', function(event) {
        if (event.target && (event.target.id.startsWith('new') || event.target.id.startsWith('edit'))) {
            event.target.classList.remove('error-field');
            const errorMsg = event.target.parentNode.querySelector('.error-message');
            if (errorMsg) {
                errorMsg.remove();
            }
        }
    });
    
    // Добавляем обработчик для отображения количества символов в описании
    document.addEventListener('input', function(event) {
        if (event.target && (event.target.id === 'newDescription' || event.target.id === 'editDescription')) {
            const charCount = event.target.value.length;
            const maxLength = 2000;
            
            // Находим или создаем элемент для отображения счетчика
            let counter = event.target.parentNode.querySelector('.char-counter');
            if (!counter) {
                counter = document.createElement('div');
                counter.className = 'char-counter';
                counter.style.fontSize = '12px';
                counter.style.color = '#666';
                counter.style.marginTop = '5px';
                event.target.parentNode.appendChild(counter);
            }
            
            counter.textContent = `${charCount}/${maxLength} символов`;
            
            if (charCount > maxLength) {
                counter.style.color = '#f44336';
            } else if (charCount > maxLength * 0.8) {
                counter.style.color = '#FF9800';
            } else {
                counter.style.color = '#666';
            }
        }
    });
});

// Экспортируем функции для глобального использования
window.fillFilmList = fillFilmList;
window.loadFilmForEdit = loadFilmForEdit;
window.deleteFilm = deleteFilm;
window.addFilm = addFilm;
window.submitNewFilm = submitNewFilm;
window.updateStats = updateStats;