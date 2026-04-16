# Git 笔记

> &emsp;&emsp;**版本控制**这东西，一开始觉得麻烦，但是建立好后后期维护修改会方便很多（实验室写代码、做文档、改论文都可以用 Git）。
> &emsp;&emsp;这篇文章不是官方文档，是我自己从零学 Git 时整理的东西。(有错误请指正！)

## 0. why？使用Git

试想一下，在写代码、文档的时候，你可能遇到以下问题：

- 改了一版代码，结果发现之前的版本更好，想回退。
- 想同时在不同的功能上开发，怕互相影响。
- 想试试一个新方案，怕改了之后忘了原来的代码长什么样，于是复制了一堆文件夹；
- 实验室一起合作赶项目，改完互相覆盖，修改的不知道在哪个版本了。

Git 就是为了解决这些问题而生的。它可以帮你：
- 记录每一次修改&emsp;->&emsp;就跟打游戏存档一样。
- 随时回退到任意一个历史版本；
- 同时开发多条“平行世界”（分支），最终再合并；
- 和别人协作，自动合并修改，避免覆盖。

Git 是**本地运行**的（你电脑上），搭配 **GitHub **或 GitLab 可以云同步和协作。

---


## 1. 我一般什么时候用 Git

&emsp;git 是个工具，什么时候用它取决于你的需求。对于我们实验室的小项目，我一般在以下情况下使用 Git：

- 开始一个新项目：`git init` 或者从 GitHub `git clone` 一个模板;
- 每天开始干活前：`git pull --rebase` 拉取最新代码;
- 写完一个功能：`git add .` + `git commit -m "xxx"`;
- 想同步到 GitHub：`git push origin main`;
- 改乱了想回退：`git reset` 或 `git checkout`;

<span style="font-size:14px;opacity:0.8;">
&emsp;当然，如果只是写个小脚本或者临时代码，可能就不需要 Git，直接放在电脑上就好了。Git 最适合管理**持续迭代**的项目，尤其是多人协作的项目。
</span>

---

## 第一部分：准备

### 2.安装 Git

- #### Windows
去 [git-scm.com](https://git-scm.com/) 下载安装包，一路默认下一步就行。装完后在开始菜单找到 “Git Bash”，打开是一个黑窗口，就可以用 Git 命令了。

- #### Linux（Ubuntu）
一般自带 Git，如果没有可以用包管理器安装，

```bash
sudo apt update
sudo apt install git
```

<span style="font-size:14px;opacity:0.8;">
&emsp;装完后，在任何文件夹里右键（Windows）或打开终端，输入 git --version 看到版本号就成功了。
</span>

### 3.（第一次）配置 Git

Git 需要知道你是谁，因为每次提交都会记录作者。

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

<span style="font-size:14px;opacity:0.8;">
` --global ` 表示这台电脑上所有仓库都用这个信息。<br>如果某个仓库想用不同的名字，可以在那个仓库里去掉 ` --global ` 重新设置。

</span>

---

## 第二部分：中间部分（日常使用）
这一章是 Git 最核心的内容，覆盖了你每天都会用到的命令和概念。

### 4.初始化一个仓库
假设你有一个文件夹叫 `my_project`，里面有一些代码。你想让 Git 管理它。

打开终端 &emsp; <em>(学会终端很重要！)</em>&emsp;，进入这个文件夹：

```bash
cd path/to/my_project
```

然后运行：
```bash
git init
```

你会看到输出：`Initialized empty Git repository in .../.git/`。
这个 `.git `文件夹就是 Git 的“数据库”，不要动它。
现在 Git 已经开始跟踪这个文件夹了，但目前还没有记录任何版本。

### 5.Git的三个区域！（要理解）
Git 有三个主要区域：
- **工作区（Working Directory）**：你平时编辑代码的地方，就是你的文件夹。
- **暂存区（Staging Area）**：你告诉 Git 你想提交哪些文件的地方。可以理解为一个“待办清单”。
- **版本库（Repository）**：Git 存储提交历史的地方，每次提交都会在这里记录一个快照。

**流程是：**
`工作区修改`→`git add`→`暂存区`→`git commit`→`仓库`
---

### 6. 最常用的命令

| 命令 | 作用 | 使用场景/备注 |
|------|--------|----------|
| `git init` | 初始化仓库 | 新建项目时 |
| `git remote add origin [url]` | 添加远程仓库 | 将本地仓库与远程仓库关联 |
| `git status` | 看当前改了哪些文件 | 每次操作前都看一眼，防止搞错 |
| `git add <file>` | 把文件加到暂存区 | 一般用 `git add .` 全部加 |
| `git commit -m "msg"` | 提交 | 消息写清楚，别写“update” |
| `git push origin main` | 推送到远程 | 先 pull 再 push |
| `git pull --rebase` | 拉取并变基 | 比普通 pull 历史干净 |
| `git log ` | 看提交历史 | 了解项目的发展 |
| `git diff` | 看具体改了啥 | 改代码忘了改哪里时用 |
| `git checkout -b new_branch` | 创建并切换到新分支 | 做新功能时用 |
| `git merge branch_name` | 合并分支 | 合并完可以删分支 |

### 7. 实际操作：从零开始一个项目

假设你新建了一个文件夹 `learn_git`，里面放一个 `hello.py`，内容如下：

```python
print("hello")
```

- 步骤1：初始化 Git

```bash
cd learn_git
git init
```

- 步骤2：添加文件到暂存区

```bash 
git add hello.py
git commit -m "第一次提交：添加 hello.py"
```

- 步骤3：修改文件，再次提交

```python
print("hello, Git!")
```

然后：

```bash
git status   # 会看到 hello.py 被修改了，显示红色
git add hello.py
git commit -m "第二次提交：修改 hello.py"
```

- 步骤4：查看提交历史

```bash
git log --online
```

输出类似：
```bash
3a2b1c0 修改输出为 hello world
1a2b3c4 第一次提交：添加 hello.py
```

### 8.版本回退——后悔药

1. 情况a：改了代码但还没 add（工作区改乱了）
想直接丢弃工作区的改动，回到上一次 commit 的状态

```bash
git checkout -- hello.py
```
注意：这个操作不可恢复，确认不要了再执行。

2. 情况b：已经 add 了但还没 commit（暂存区有内容，想撤回）
```bash
git reset HEAD hello.py
```
这会把它从暂存区移出，但工作区的改动还在。
如果想彻底丢弃工作区的改动，再执行 `git checkout -- <文件名>`

3. 情况c：已经 commit 了（版本库乱了）
先用 git log --oneline 找到你想回去的 commit ID（比如 1a2b3c4），然后：
- 想回退到上一个版本（保留改动）
```bash
git reset --soft HEAD~1
```
- 想回退到上一个版本（丢弃改动）
```bash
git reset --hard HEAD~1
```

<span style="font-size:14px;opacity:0.8;">

注意：--hard 会丢弃之后的所有改动，并且无法恢复（除非用 git reflog 找回来）。谨慎使用。

如果你只是想“看看”以前的版本，不丢失当前工作，可以用 git checkout 1a2b3c4，看完再切回来：git checkout main。

</span>

## 9. 分支：平行宇宙

分支是 Git 最强大的功能。你可以从主分支（main）分出一个支线，在里面做实验、开发新功能，不影响主分支。实验成功了，再合并回来。

**基本操作**
- 查看所有分支：&emsp;`git branch`（当前分支前面有个 *）
- 创建新分支：&emsp;&emsp;`git branch 分支名`
- 切换到新分支：&emsp;`git checkout 分支名`（或者用 `git switch 分支名`，更直观）
- 创建并切换：&emsp;&emsp;`git checkout -b 新分支名`
- 合并分支：&emsp;&emsp;&emsp;先切回 main，然后 `git merge 新分支名`

**举个实际例子**
你正在写 `main.c`，突然想到一个改进想法，但不确定能不能成。

```bash
git checkout -b experiment    # 创建并切换到  experiment 分支
# 在 experiment 分支里疯狂改代码，测试
git add .
git commit -m "实验性改动"
```

如果实验失败，直接切回main分支，然后删除experiment 分支：

```bash
git checkout main
git branch -d experiment
```

如果实验成功，合并到 main：
```bash
git checkout main
git merge experiment
```

## 10.远程仓库：GitHub 协作
假设你和师弟一起做项目，仓库在 GitHub 上。

**师兄（项目发起人）：**
1. 在 GitHub 建仓库，把初始代码 push 上去。
2. 去仓库的 Settings → Collaborators，添加师弟的 GitHub 账号（需要师弟同意）。

**师弟：：**
1. 收到邀请邮件后接受。
2. 克隆仓库：`git clone https://github.com/师兄/项目名.git`
3. 开始干活：改代码 → `git add` → `git commit` → `git push origin main`
4. 如果 push 被拒绝（说明师兄先 push 了新的），先 `git pull --rebase`，解决冲突，再 push。

**注意**：尽量不要直接在 main 分支上开发，各自建分支更安全。流程：
```bash
git checkout -b feature/add_sensor
# 开发，提交
git push origin feature/add_sensor
```
然后在 GitHub 上创建一个 Pull Request，师兄审核后合并。


---

## 第四部分： 我踩过的坑（真实经历）

| 现象 | 原因 | 解决方法 |
|------|------|----------|
| `git push` 被拒绝 | 远程有别人提交的更新 | 先 `git pull --rebase`，再 push |
| `git push` 后提示 "merge conflict" | 	远程和本地改了同一处 | 打开冲突文件，手动解决，然后 `git add .` + `git commit` |
| `git commit` 后想改 commit 信息| 	消息写错了 | `git commit --amend -m "新的消息"`（只适合最后一次 commit） |
| `git reset --hard` 后丢了好多代码| 手贱 | 不要慌，`git reflog` 找到之前的 commit ID，`git reset --hard 那个ID `就能回来 |

<span style="font-size:14px;opacity:0.8;">

**其他小技巧**<br>
- 想看某个文件的历史：
`git log -- <file>`。<br>
- 想看某次提交改了哪些文件：
`git show --name-only <commit_id>`。<br>
- 暂存当前改动：正在改代码，突然要切到别的分支修 bug，又不想提交半成品。
```bash
git stash              # 存起来
git checkout other_branch
# 修完 bug 切回来
git stash pop          # 恢复
```

- 提交信息怎么写：推荐格式 <类型>: 简短说明。类型可以是：

    - feat: 新功能
    - fix: 修 bug
    - docs: 文档
    - refactor: 重构代码
    - chore: 杂项（改配置、加 gitignore 等）
**例如**：
feat: 添加MPU6050驱动、
fix: 修复串口初始化失败。
（这样看 log 非常清晰）

</span>

---

## 第五部分： 我的 .gitignore 模板

实验室项目一般是单片机代码 + Python 脚本，我一般放这些：

```gitignore
# 编译中间文件
*.o
*.d
*.hex
*.bin
*.elf

# IDE 配置（不同人配置不一样）
.vscode/
.idea/
*.swp
*.swo

# Python 缓存
__pycache__/
*.pyc

# 系统文件
.DS_Store
Thumbs.db

# 敏感信息
*.pem
*.key
*.secret
```




## 第六部分：学习资源
- **Pro Git 中文版**：官方书，免费在线阅读 [git-scm.com/book/zh/v2](https://git-scm.com/book/zh/v2)。不需要全看，先看第1-3章。
- **简单备忘录**：一个html页面，速查用 [training.github.com](https://training.github.com/)
- **B站视频**：搜索“Git 教程 黑马程序员”，一小时左右，跟着敲一遍就能上手。
- **菜鸟教程**：[runoob.com/git](https://www.runoob.com/git/git-tutorial.html)，适合查命令用。

> 最后说一句：Git 不要死记硬背，用着用着就熟了。刚开始只需要记住 `add`、`commit`、`push`、`pull` 就够了，遇到问题再搜。希望这篇文章能帮你少走一些弯路。

---

<p align="center">
总之，Git 是个强大的工具，学会了它就能更好地管理代码和协作。希望这些笔记对你也有帮助！<br>
salute to Git! 🚀
</p>
