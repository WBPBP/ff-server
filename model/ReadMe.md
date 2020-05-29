# model
 
  안드로이드로부터 특징값을 입력받아 몸의 균형 및 걸음걸이 패턴을 분석해주는 모델입니다.
  
## API

### walkData

 총 5가지 걸음걸이 특징값들과 걸음걸이 패턴에 맞는 comment를 저장해놓은 파일입니다.
 
  · `normalGait` : 올바른 걸음걸이 특징값을 저장해놓은 클래스
    - `getLeft` : 왼발의 특징값을 반환
    - `getRight` : 오른발의 특징값을 반환
    
  · `out_toedGait` : 팔자 걸음걸이 특징값을 저장해놓은 클래스
    - `getLeft` : 왼발의 특징값을 반환
    - `getRight` : 오른발의 특징값을 반환
    
  · `in_toedGait` : 안짱 걸음걸이 특징값을 저장해놓은 클래스
    - `getLeft` : 왼발의 특징값을 반환
    - `getRight` : 오른발의 특징값을 반환
    
  · `craneGait` : 학다리 걸음걸이 특징값을 저장해놓은 클래스
    - `getLeft` : 왼발의 특징값을 반환
    - `getRight` : 오른발의 특징값을 반환
    
  · `elevenGait` :11자 걸음걸이 특징값을 저장해놓은 클래스
    - `getLeft` : 왼발의 특징값을 반환
    - `getRight` : 오른발의 특징값을 반환
    
  
### dataProccessing

 안드로이드로부터 입력받은 특징값을 분석해 결과를 json형식으로 반환해주는 파일입니다.
 
  - `analysisStaticPressureResulr` : 
     
  
