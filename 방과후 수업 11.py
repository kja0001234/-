import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("진자 운동 시뮬레이션")

# 입력값
length = st.slider("진자 길이 (m)", 0.1, 10.0, 1.0)
theta0_deg = st.slider("초기 각도 (도)", 1, 90, 30)
speed = st.slider("시뮬레이션 속도 (배속)", 0.1, 10.0, 1.0, step=0.1)  # 최대 10배속

g = 9.81  # 중력 가속도 m/s²

theta0 = np.radians(theta0_deg)  # 초기 각도 라디안 변환

# 단순 조화 진동 근사 (감쇠 무시)
T = 2 * np.pi * np.sqrt(length / g)  # 주기

frame_count = 500
t = np.linspace(0, 4 * T, frame_count)  # 4주기 동안

omega = np.sqrt(g / length)  # 각진동수
theta_t = theta0 * np.cos(omega * t)  # 각도 변화

# 진자의 각속도, 각가속도 계산
angular_velocity = -theta0 * omega * np.sin(omega * t)
angular_acceleration = -theta0 * omega**2 * np.cos(omega * t)

# x, y 좌표 계산 (진자 위치)
x = length * np.sin(theta_t)
y = -length * np.cos(theta_t)

fig = go.Figure(
    data=[go.Scatter(x=[0, x[0]], y=[0, y[0]], mode="lines+markers", line=dict(width=3), marker=dict(size=12))],
    layout=go.Layout(
        xaxis=dict(range=[-length-0.5, length+0.5], zeroline=False, showgrid=False),
        yaxis=dict(range=[-length-0.5, 0.5], zeroline=False, showgrid=False),
        title="진자 운동",
        width=600,
        height=600,
        autosize=False,
        showlegend=False,
        yaxis_scaleanchor="x",
    ),
)

# 애니메이션 프레임 생성
frames = [
    go.Frame(
        data=[go.Scatter(x=[0, x[k]], y=[0, y[k]], mode="lines+markers", line=dict(width=3), marker=dict(size=12))]
    )
    for k in range(frame_count)
]

fig.frames = frames

# 애니메이션 버튼, 슬라이더 설정
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            y=1,
            x=1.15,
            xanchor="right",
            yanchor="top",
            buttons=[
                dict(
                    label="▶ Play",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": max(1, int(20 / speed)), "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0},
                        },
                    ],
                )
            ],
        )
    ],
    sliders=[
        dict(
            steps=[
                dict(
                    method="animate",
                    args=[
                        [f.name],
                        {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}},
                    ],
                    label=str(i),
                )
                for i, f in enumerate(fig.frames)
            ],
            active=0,
            y=0,
            x=0,
            len=1.0,
        )
    ],
)

st.plotly_chart(fig)

# 진자 운동 분석 결과 출력
st.subheader("진자 운동 분석 값")
st.write(f"- 진자 길이: {length:.2f} m")
st.write(f"- 초기 각도: {theta0_deg}° ({theta0:.2f} rad)")
st.write(f"- 주기 (T): {T:.3f} 초")
st.write(f"- 각진동수 (ω): {omega:.3f} rad/s")

max_angular_velocity = np.max(np.abs(angular_velocity))
max_linear_velocity = max_angular_velocity * length
max_angular_acceleration = np.max(np.abs(angular_acceleration))
max_linear_acceleration = max_angular_acceleration * length

st.write(f"- 최대 각속도: {max_angular_velocity:.3f} rad/s")
st.write(f"- 최대 선속도: {max_linear_velocity:.3f} m/s")
st.write(f"- 최대 각가속도: {max_angular_acceleration:.3f} rad/s²")
st.write(f"- 최대 선가속도: {max_linear_acceleration:.3f} m/s²")
