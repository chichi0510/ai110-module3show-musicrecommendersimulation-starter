# Model Card: Music Recommender Simulation

## 1. Model Name

**TuneTaste Lite**

---

## 2. Goal / Task

This model suggests **songs from a small catalog** that **fit a user’s stated taste**. It does **not** predict a single “correct” answer. Instead, it scores every track for **how well its tags and energy match** the user’s profile, then recommends the **best-matching** ones. Think: “find rows that look like what you asked for,” not “guess what you will click next with machine learning.”

---

## 3. Data Used

- **Size:** **18** songs in `data/songs.csv` (**10** from the starter file **plus 8** added for more genre and mood variety).
- **Features used in scoring:** **genre** (text), **mood** (text), **energy** (number from 0 to 1).
- **Also in the file but not used in the default score:** **tempo_bpm**, **valence**, **danceability**, **acousticness** (available for future experiments).
- **Limits:** The catalog is **small**, **hand-made**, and **not** a sample of real streaming behavior. Some genres appear more often than others, so the recommender can **reflect dataset imbalance**, not real-world popularity.

---

## 4. Algorithm Summary

The system walks through **every song** in the table. For each one it adds points in three parts:

1. **Genre:** If the song’s genre label **exactly matches** the user’s favorite genre, it gets a **fixed bonus** (default **+2** points). If not, it gets **no** genre bonus.
2. **Mood:** If the song’s mood label **exactly matches** the user’s favorite mood, it gets another **fixed bonus** (default **+1** point). If not, **no** mood bonus.
3. **Energy:** The model does **not** reward “higher energy is always better.” It rewards **closeness** to the user’s **target energy**: the smaller the gap between song energy and target, the larger the extra score (up to **+1** when they are the same).

The **total score** is the sum of those parts. Then **all songs are sorted** from **highest score to lowest**, and the top **k** (for example five) are returned. Optional experiments can change the point values or scale energy, but the **idea stays the same:** match labels, then fine-tune with energy, then rank.

---

## 5. Observed Behavior / Biases

In testing, three very different user profiles (**pop/happy/high energy**, **lofi/chill/low energy**, **rock/intense/high energy**) produced **different top songs**, which shows the rules react to the profile.

We also saw real **weak spots**:

- **Genre-first behavior:** A song like **Gym Hero** (pop but **intense** mood) can still rank high for a **pop + happy** user because **genre match** is large and **mood** does not have to match for partial credit—so the system can feel **more loyal to genre than to mood**.
- **Same songs in many lists:** High-energy tracks with **no genre match** can still appear mid-list for other profiles **only** because of **energy similarity**. That is expected from the math, but it can look odd if you forget energy is always in play.
- **Label bias:** **Indie pop** does not count as **pop** unless the strings match. That can **hide** good matches that are “close” in real life.
- **Filter bubble risk:** If someone always keeps the same profile, the same **genre cluster** can keep winning—there is **no** built-in “try something new” step.

---

## 6. Evaluation Process

Evaluation was **manual and profile-based**, not a single accuracy number.

1. **Stress tests:** I ran **three** fixed profiles in `src/main.py` and checked whether **top recommendations** matched my **music intuition** (upbeat pop vs calm lofi vs intense rock).
2. **Weight-shift experiment:** For the **Chill Lofi** user, I compared **default** scoring to a version with **lower genre weight** and **doubled energy weight**. I compared **top-five lists** before and after to see if **rankings** moved.
3. **Reason strings:** I read the printed **reasons** for each song to confirm the score matched the story (genre/mood/energy).

This process checks **whether the system behaves differently when inputs differ**, and **whether small rule changes change the list**—not whether one song is objectively “right.”

---

## 7. Intended Use and Non-Intended Use

### Intended use

- **Teaching and homework:** Show how **content-based** matching, **scoring**, and **ranking** fit together.
- **Demos and prototypes:** Quick “what if” runs with fake users and a tiny catalog.
- **Discussion of bias:** Clear rules make it easy to ask *why* a song was recommended.

### Non-intended use

- **Real music products** (Spotify-scale listening, ads, or payouts).
- **High-stakes decisions** (employment, credit, health, legal outcomes).
- **Diverse or fair representation** across artists or cultures without **extra** design—this model does **not** measure fairness across groups.
- **Replacing** collaborative filtering or modern personalization; it is **rules only**, no learning from clicks or history.

---

## 8. Ideas for Improvement

1. **More songs and labels** so genre and mood are less sparse, or **synonyms** so “indie pop” can relate to “pop.”
2. **Use more columns** from the CSV (**danceability**, **valence**, **acousticness**) with matching user targets.
3. **Diversity rules** so the top five are not five near-copies (for example cap repeats of the same genre).
4. **Optional collaborative layer** (what similar users liked) on top of content features.
5. **Log real choices** (likes, skips) later, instead of only a static profile.

---

## 9. Personal Reflection

### What was your biggest learning moment?

I saw that a recommender does **not** have to start with neural networks. **Features**, a **user profile**, a **score**, and a **sort** are enough to build something you can **run, test, and explain**. Connecting those four pieces was the clearest “aha” for me.

### How did using AI tools help you, and when did you need to double-check them?

AI was useful for **structuring** the project: file layout, README sections, and boilerplate. It also sped up **brainstorming** names and edge cases. I still had to **verify** the **scoring math**, **CSV field names**, and **rubric** myself—generated code can run but miss a requirement (for example exact **reason** strings or test expectations). The **weights** and **profile design** had to match *my* intent, not whatever the model suggested first.

### What surprised you about how simple algorithms can still “feel” like recommendations?

Even with **plain addition** and string matches, **different profiles** got **different top fives** that often “felt right.” That showed me that a lot of **recommendation flavor** can come from **reasonable rules**, not only from complexity—as long as you are honest about **limits** and **bias**.

### What would you try next if you extended this project?

I would add a **small web or CLI menu** to switch profiles without editing code, grow the **dataset**, try a **diversity bonus**, and compare this **content-based** setup to a **tiny collaborative** mock (fake user–song matrix) to see when behavior diverges.
