<p align="center">
  <img src="assets/hero.svg" width="100%" alt="r33hab: app developer, AI and neural networks">
</p>

<p align="center">
  <img src="assets/terminal.svg" width="49%" alt="Terminal: whoami prints r33hab">
  <img src="assets/training.svg" width="49%" alt="Training run: loss falls while accuracy rises">
</p>

<img src="assets/divider.svg" width="100%" alt="">

## `01` What I do

<table>
<tr>
<td width="50%" valign="top">

### 📱 Apps

Multi-year app developer. Native macOS and iOS in Swift and SwiftUI, Android in Kotlin, web front ends in TypeScript and React. End to end: UI, backend, release.

</td>
<td width="50%" valign="top">

### 🧠 Neural networks

I design, build and train my own neural networks: choosing the architecture, writing the training loop, tuning until the loss curve behaves. Python and PyTorch.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ⚙️ Platforms and DevOps

Multi-tenant platforms in C# and .NET with React front ends: OIDC single sign-on, versioned SQL migrations, structured logging. Containerised and shipped to Kubernetes through CI pipelines and GitOps with Argo CD.

</td>
<td width="50%" valign="top">

### 🤖 AI agents

Tooling on top of LLMs: MCP servers that let agents work with real business systems, Agent SDK bots, and a 3D stage that shows AI agents building a project live.

</td>
</tr>
</table>

## `02` Commit to cluster

Every merge builds, tests and packages a container. Argo CD syncs the desired state from git, and Kubernetes rolls it out.

<p align="center">
  <img src="assets/pipeline.svg" width="100%" alt="CI/CD pipeline: git push, CI, container image, Argo CD sync, Kubernetes rolling update">
</p>

## `03` Stack

<p align="center">
  <sub><b>apps</b></sub><br>
  <img src="https://skillicons.dev/icons?i=swift,kotlin,ts,js,react,nodejs,html,css" alt="Swift, Kotlin, TypeScript, JavaScript, React, Node.js, HTML, CSS">
</p>
<p align="center">
  <sub><b>backend and platform</b></sub><br>
  <img src="https://skillicons.dev/icons?i=cs,dotnet,java,docker,kubernetes,githubactions,git,linux" alt="C#, .NET, Java, Docker, Kubernetes, GitHub Actions, Git, Linux"><br>
  <sub>plus Argo CD · Traefik · Keycloak / OIDC · SQL Server · Loki</sub>
</p>
<p align="center">
  <sub><b>ai and ml</b></sub><br>
  <img src="https://skillicons.dev/icons?i=py,pytorch,tensorflow" alt="Python, PyTorch, TensorFlow">
</p>

## `04` Featured builds

<p align="center">
  <a href="https://github.com/r33hAB/claude-agent-visualizer"><img width="49%" alt="claude-agent-visualizer" src="https://github-readme-stats.vercel.app/api/pin/?username=r33hAB&repo=claude-agent-visualizer&bg_color=282828&title_color=fabd2f&text_color=ebdbb2&icon_color=fe8019&border_color=3c3836&border_radius=14"></a>
  <a href="https://github.com/r33hAB/MacUninstaller"><img width="49%" alt="MacUninstaller" src="https://github-readme-stats.vercel.app/api/pin/?username=r33hAB&repo=MacUninstaller&bg_color=282828&title_color=fabd2f&text_color=ebdbb2&icon_color=fe8019&border_color=3c3836&border_radius=14"></a>
  <a href="https://github.com/r33hAB/SteamIdler"><img width="49%" alt="SteamIdler" src="https://github-readme-stats.vercel.app/api/pin/?username=r33hAB&repo=SteamIdler&bg_color=282828&title_color=fabd2f&text_color=ebdbb2&icon_color=fe8019&border_color=3c3836&border_radius=14"></a>
  <a href="https://github.com/r33hAB/discord-follow-counter"><img width="49%" alt="discord-follow-counter" src="https://github-readme-stats.vercel.app/api/pin/?username=r33hAB&repo=discord-follow-counter&bg_color=282828&title_color=fabd2f&text_color=ebdbb2&icon_color=fe8019&border_color=3c3836&border_radius=14"></a>
</p>

## `05` Telemetry

<p align="center">
  <img height="160" alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=r33hAB&show_icons=true&count_private=true&include_all_commits=true&rank_icon=github&bg_color=282828&title_color=fabd2f&text_color=ebdbb2&icon_color=fe8019&ring_color=d3869b&border_color=3c3836&border_radius=14">
  <img height="160" alt="Contribution streak" src="https://streak-stats.demolab.com?user=r33hAB&background=282828&border=3C3836&stroke=3C3836&ring=FE8019&fire=FB4934&currStreakNum=EBDBB2&sideNums=EBDBB2&currStreakLabel=FABD2F&sideLabels=A89984&dates=928374&border_radius=14">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/r33hAB/r33hAB/output/snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/r33hAB/r33hAB/output/snake-light.svg">
    <img width="100%" alt="A snake eating the contribution graph" src="https://raw.githubusercontent.com/r33hAB/r33hAB/output/snake-dark.svg">
  </picture>
</p>

<details>
<summary><code>&gt;&gt;&gt; model.summary()</code></summary>

```text
Model: "r33hab"
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Layer (type)            ┃ Output shape   ┃ Params       ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ curiosity (Input)       │ (None, ∞)      │ 0            │
│ app_dev (Dense)         │ (None, years)  │ lots         │
│ dotnet_platform (Dense) │ (None, k8s)    │ multi-tenant │
│ gitops (ArgoSync)       │ (None, synced) │ auto         │
│ neural_nets (Dense)     │ (None, 256)    │ self-trained │
│ coffee (Dropout)        │ (None, 256)    │ 0            │
│ ship (Output)           │ (None, 1)      │ 1            │
└─────────────────────────┴────────────────┴──────────────┘
 Trainable params: all of them
 Non-trainable params: 0
```

</details>

<img src="assets/divider.svg" width="100%" alt="">

<p align="center"><sub>forward pass · backprop · ship · repeat</sub></p>
