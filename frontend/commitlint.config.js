export default {
  /* Создаем собственный плагин для проверки регулярным выражением */
  plugins: [
    {
      rules: {
        'custom-issue-status-pattern': (parsed) => {
          const { header } = parsed;
          const pattern = /^(?:(?:#|[A-Z]+-)?\d+\s+)?\[[^\]]+\]:\s+.+$/;

          const isValid = pattern.test(header);

          return [
            isValid,
            `Ваш коммит должен соответствовать паттерну -> "номер_ишью статус: тело" или "номер_ишью: тело"\n` +
            `Пример 1: #123 [In Progress]: Добавил валидацию формы\n` +
            `Пример 2: PROJ-456: Исправил баг с отображением`,
          ];
        },
      },
    },
  ],
  /* Включаем наше созданное правило */
  rules: {
    'custom-issue-status-pattern': [2, 'always'],
  },
};