// Функция для заполнения таблицы фильмами
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                // Ячейка с русским названием
                let tdTitleRus = document.createElement('td');
                tdTitleRus.innerHTML = films[i].title_ru;
                
                // Ячейка с оригинальным названием (если отличается)
                let tdTitle = document.createElement('td');
                tdTitle.innerHTML = films[i].title === films[i].title_ru ? '' : films[i].title;
                if (tdTitle.innerHTML) {
                    tdTitle.style.fontStyle = 'italic';
                    tdTitle.style.color = '#666';
                }
                
                // Ячейка с годом
                let tdYear = document.createElement('td');
                tdYear.innerHTML = films[i].year;
                
                // Ячейка с действиями
                let tdActions = document.createElement('td');
                
                // Кнопка редактирования
                let editButton = document.createElement('button');
                editButton.innerHTML = 'редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                };
                editButton.style.marginRight = '10px';
                editButton.style.padding = '5px 10px';
                editButton.style.background = '#FF9800';
                editButton.style.color = 'white';
                editButton.style.border = 'none';
                editButton.style.borderRadius = '3px';
                editButton.style.cursor = 'pointer';
                
                // Кнопка удаления
                let delButton = document.createElement('button');
                delButton.innerHTML = 'удалить';
                delButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };
                delButton.style.padding = '5px 10px';
                delButton.style.background = '#f44336';
                delButton.style.color = 'white';
                delButton.style.border = 'none';
                delButton.style.borderRadius = '3px';
                delButton.style.cursor = 'pointer';
                
                // Добавляем кнопки в ячейку
                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);
                
                // Добавляем ячейки в строку
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdTitle);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);
                
                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            }
        })
        .catch(function (error) {
            console.error('Ошибка загрузки фильмов:', error);
            document.getElementById('film-list').innerHTML = 
                '<tr><td colspan="4" style="color: red; text-align: center;">Ошибка загрузки данных</td></tr>';
        });
}

// Функция удаления фильма
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(function(response) {
        if (response.status === 204) {
            // Перезагружаем таблицу после удаления
            fillFilmList();
        } else {
            alert('Ошибка при удалении фильма');
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при удалении фильма');
    });
}

// Функция редактирования фильма
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function(response) {
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
            output.innerHTML = `<h3>Редактирование фильма #${id}</h3>
                              <p>Заполните форму выше и нажмите "Обновить фильм"</p>`;
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            alert('Ошибка при загрузке данных фильма');
        });
}

// Функция добавления нового фильма
function addFilm() {
    // Очищаем форму добавления
    document.getElementById('newTitle').value = '';
    document.getElementById('newTitleRu').value = '';
    document.getElementById('newYear').value = '';
    document.getElementById('newDescription').value = '';
    
    // Показываем сообщение
    const output = document.getElementById('output');
    output.innerHTML = '<h3>Добавление нового фильма</h3>' +
                      '<p>Заполните форму "Добавить новый фильм" выше</p>';
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});