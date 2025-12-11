# TDD 방법론을 사후적으로 적용

현재 프로젝트 진행 과정에서 test 코드가 구현이 안되어 있어서 코드 변경에서 side effect를 예측할 수 없는 상황입니다.

이를 제어하기 위해 사후적으로 TDD를 적용하여 추후 개발되는 것들이 기존 코드에 영향을 주는 일이 없도록 할 예정입니다. 

그래서 1.4 버전에선 TDD를 위한 테스트 코드를 작성하기에 앞서 TDD를 범용적으로 진행할 수 있는 문서만 작성할 예정입니다.

- tests/principle.md : 모든 TDD에서 지켜야할 TDD 방법론 제시시
- tests/TEST_README_TEMPLATE.md: 해당 프로젝트에서 지켜야할 실천적 TDD의 룰을 작성할 탬플릿
- tests/README.md: 해당 프로젝트에서 지켜야할 실천적 TDD의 룰
- tests/workflow_template.yaml: 해당 프로젝트에서 사용할 기본적 github actions CI/CD의 탬플릿 

일단 여기까지만 작성해서 문서 자체를 프로젝트에 포함시킨 걸 v2.0으로 할 생각이야 