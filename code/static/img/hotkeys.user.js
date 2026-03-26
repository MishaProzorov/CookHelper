// ==UserScript==
// @name         FC Database Manager Hotkeys
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Горячие клавиши для FC Database Manager (Streamlit)
// @author       You
// @match        http://localhost:8501/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Функция для клика по кнопке по тексту
    function clickButtonByText(text) {
        const buttons = document.querySelectorAll('button[kind]');
        for (let button of buttons) {
            if (button.textContent.includes(text)) {
                button.click();
                return true;
            }
        }
        return false;
    }

    // Функция для клика по кнопке по data-testid
    function clickButtonByTestId(testId) {
        const button = document.querySelector(`button[data-testid="${testId}"]`);
        if (button) {
            button.click();
            return true;
        }
        return false;
    }

    // Обработчик горячих клавиш
    document.addEventListener('keydown', function(e) {
        // Проверяем, что фокус не на input/textarea
        const tagName = document.activeElement.tagName.toLowerCase();
        const isInput = tagName === 'input' || tagName === 'textarea' || tagName === 'select';

        // Ctrl комбинации
        if (e.ctrlKey && !isInput) {
            switch(e.key.toLowerCase()) {
                case 'a': // Добавить запись
                    e.preventDefault();
                    clickButtonByText('➕ Добавить') || clickButtonByText('Добавить новую');
                    break;
                case 'v': // Просмотр таблицы
                    e.preventDefault();
                    clickButtonByText('🗄️ Таблицы') || clickButtonByText('Таблицы');
                    break;
                case 'd': // Удалить запись
                    e.preventDefault();
                    clickButtonByText('🗑️ Удалить') || clickButtonByText('Удалить запись');
                    break;
                case 'u': // Редактировать запись
                    e.preventDefault();
                    clickButtonByText('✏️ Редактировать') || clickButtonByText('Редактировать');
                    break;
                case 'q': // Специальный запрос
                    e.preventDefault();
                    clickButtonByText('📈 Аналитика') || clickButtonByText('Аналитика');
                    break;
                case 's': // Сохранить результат
                    e.preventDefault();
                    clickButtonByText('📥 Сохранить') || clickButtonByText('Скачать Excel');
                    break;
                case 'b': // Бэкап
                    e.preventDefault();
                    clickButtonByText('💾 Бэкап') || clickButtonByText('Создать бэкап');
                    break;
                case 'e': // Выход
                    e.preventDefault();
                    clickButtonByText('🚪 Выход');
                    break;
            }
        }

        // F10 - меню
        if (e.key === 'F10') {
            e.preventDefault();
            clickButtonByText('📋 Меню') || clickButtonByText('Меню');
        }

        // Esc - закрыть диалог (клик по Cancel)
        if (e.key === 'Escape') {
            clickButtonByText('Cancel') || clickButtonByText('❌ Cancel');
        }
    });

    console.log('FC Database Manager Hotkeys loaded!');
})();
