# 🎵 Music Trends & Global Listening Patterns (CS467 Capstone Project)

> 교환학생 시절 CS467 캡스톤 과목에서 진행한 빅데이터 프로젝트입니다. Spotify 트랙/오디오 특성 데이터와 Million Musical Tweets Dataset(MMTD)을 결합해, 음악의 인기·가사·화성적 특징이 시간·지역에 따라 어떻게 변화하는지 다각도로 분석했습니다.

> 📌 팀 프로젝트로, 이 리포지토리는 팀원 리포지토리에서 시작해 개인 정리한 버전입니다.

## 📖 프로젝트 소개

"어떤 음악이 왜, 어디서 인기를 얻는가?"라는 질문에 데이터로 답해보고자 한 프로젝트입니다. 여러 공개 음악 데이터셋(Spotify API, MMTD 트윗 데이터, 가사 데이터셋)을 병합해 다음 네 가지 분석을 진행했습니다.

| 분석 주제 | 내용 |
|---|---|
| 🌍 **국가별 음악 취향 지도** | 트윗 데이터 기반으로 국가별 선호 장르를 지도에 시각화 |
| 📝 가사 가독성 변화 | 연도별 가사의 Linsear Write 가독성 점수 변화와 인기도 상관관계 |
| 🎼 화성/음색 상관관계 | 분기별 음색(Timbre) 토픽과 인기도의 상관관계 |
| 🎧 데이터 수집 | Spotify API를 통한 트랙/아티스트 메타데이터 수집 |

## 🙋‍♀️ 본인 담당 부분: 국가별 음악 취향 지도 시각화

`global_map/map.ipynb`를 담당했습니다.

- MMTD(Million Musical Tweets Dataset)의 트윗 로그와 Spotify 트랙 메타데이터를 `artist_name` + `track_title` 기준으로 병합
- 국가별로 가장 많이 언급된 장르를 집계하고, `umbrella_genre`(세부 장르를 상위 카테고리로 그룹화)로 정제해 노이즈 감소
- `geopandas`로 세계 지도(Natural Earth shapefile) 위에 국가별 선호 장르를 색상으로 매핑해 시각화
- 트윗 언급 횟수 기준 상위 인기곡과 평균 인기도(popularity)를 함께 집계해 국가 간 비교 근거로 활용

## 🛠️ 기술 스택

- **Python** — pandas, numpy (데이터 처리)
- **geopandas, matplotlib** — 지리 데이터 시각화
- **seaborn** — 상관관계 그리드 플롯 (팀원 파트)
- **Spotify Web API** — 트랙/아티스트 메타데이터 수집 (팀원 파트)
- **Jupyter Notebook** — 지도 시각화 분석 (`global_map/map.ipynb`)

## 📁 데이터 소스

- **Spotify Web API** — 트랙 오디오 특성, 아티스트 장르, 인기도
- **[nowplaying-RS Dataset](https://dbis-nowplaying.uibk.ac.at)** — 1,100만 건 이상의 트위터 기반 음악 청취 이벤트 (국가/시간대/해시태그 포함)
- **TCC CEDS Music Dataset** — 가사 및 장르 정보

## 📂 프로젝트 구조

```
DataSets/                 # 정제/병합된 트랙, 가사 데이터셋
Harmonic_correlation/     # 음색-인기도 상관관계 분석 (팀원 담당)
global_map/               # 국가별 음악 취향 지도 시각화 (본인 담당)
ReadabilityOverTime.py    # 가사 가독성 변화 분석 (팀원 담당)
spotifyAPI.py             # Spotify API 데이터 수집 스크립트 (팀원 담당)
```

## 🔒 참고

- 원본 데이터 수집에 사용된 Spotify API 인증 정보(.env)는 보안을 위해 리포지토리 히스토리에서 완전히 제거했습니다. 실행하려면 별도로 [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)에서 발급받은 `CLIENT_ID`, `CLIENT_SECRET`을 `.env` 파일에 설정해야 합니다.
