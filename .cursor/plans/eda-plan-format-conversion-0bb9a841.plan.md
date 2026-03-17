<!-- 0bb9a841-46bf-401b-a0eb-b3468e8a4bb1 -->
---
todos:
  - id: "normalize-plan-header"
    content: "Оформить plan-заголовок (comment + frontmatter + isProject)."
    status: pending
  - id: "create-eda-todos"
    content: "Сконвертировать разделы EDA в 4–6 actionable todo-пунктов."
    status: pending
  - id: "migrate-plan-body"
    content: "Перенести весь EDA-контент в тело нового plan-файла без потери структуры."
    status: pending
  - id: "save-plan-file"
    content: "Сохранить новый .plan.md файл в .cursor/plans с уникальным идентификатором."
    status: pending
isProject: false
---
# Преобразование EDA файла в формат plan

## Цель
Привести `DLS_Speech_HW/EDA_train_features_plan.md` к структуре plan-файла как в `/.cursor/plans/waveform-feature-engineering-steps-1-7-0bb9a841.plan.md`: HTML-комментарий ID, YAML frontmatter с `todos`, затем markdown-план.

## Что будет сделано
- Скопировать структуру заголовка plan-файла:
  - строка `<!-- <uuid> -->`
  - блок `---` с `todos` и `isProject: false`
  - основной markdown-контент плана.
- Перенести содержимое EDA-плана в тело документа без потери секций (`1..11`).
- Сформировать 4–6 прикладных todo-пунктов из текущего EDA текста:
  - data-quality checks,
  - distribution/outliers,
  - correlation pruning,
  - target-association ranking,
  - baseline + artifacts.
- Сохранить результат как новый plan-файл рядом с планами:
  - `/.cursor/plans/eda-train-features-<id>.plan.md`
- (Опционально) оставить в `DLS_Speech_HW/EDA_train_features_plan.md` короткую ссылку на новый plan-файл, если нужно единое место входа.

## Критерии готовности
- Файл открывается как валидный markdown с frontmatter.
- В `todos` есть понятные шаги с `status: pending`.
- Основной текст полностью отражает текущий EDA-план для `train_features_df`.
- Формат визуально и структурно соответствует примеру `waveform-feature-engineering-steps-1-7-0bb9a841.plan.md`.
