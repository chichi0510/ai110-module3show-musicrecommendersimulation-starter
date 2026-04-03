# Reflection: Comparing User Profiles

This note compares the **three stress-test profiles** defined in `src/main.py`, using plain language. The recommender always uses the same scoring recipe; only the **user’s favorite genre, mood, and target energy** change.

---

## High-Energy Pop vs Chill Lofi

The **High-Energy Pop** listener wants **pop**, **happy**, and **high** energy. The top results lean toward tracks that are literally tagged **pop** and **happy**, such as *Sunrise City*, because those rows earn the full **genre** and **mood** bonuses at once. The **Chill Lofi** listener wants **lofi**, **chill**, and **low** energy. Winners are **lofi + chill** songs like *Library Rain* and *Midnight Coding*, with calm energy that sits near the low target. The two lists look **nothing alike**: one is bright and uptempo by design, the other is soft and steady. That gap shows **energy and mood tags are doing real work**, not just genre alone.

---

## High-Energy Pop vs Deep Intense Rock

Both profiles ask for **high energy**, so many songs with **similar energy levels** can look “okay” on the **energy** line alone. The split comes from **genre and mood**: **pop + happy** rewards *Sunrise City* and other pop-tagged tracks, while **rock + intense** lifts *Storm Runner* and other rock-tagged, intense tracks. **Gym Hero** (pop but **intense** mood) can rank well for the pop user on **genre points** even when the mood does not say “happy,” which shows **genre currently outweighs mood** when both cannot match. For the rock user, **rock + intense** is the clearest path to the top—so **genre** is again the main switch between these two personas.

---

## Chill Lofi vs Deep Intense Rock

These personas are almost **opposites**: one wants **calm, low-energy lofi**, the other wants **loud, high-energy rock**. The outputs should differ a lot—and they do. The lofi profile fills the top with **lofi/chill** rows; the rock profile centers **rock/intense** and nearby energy. If the lists ever looked similar, we would worry the model was **ignoring mood or energy**; here, the **top one** for each profile matches the story we would tell a friend. The main caveat is **string matching**: a song must use the **exact** genre and mood text stored in the CSV, so “close enough” music with a different label will not get full credit.

---

## Takeaway

Different profiles produce **different top fives** because **fixed points for genre and mood** separate broad styles, and **energy similarity** fine-tunes within that space. The design is **transparent**, but it can **over-trust labels** and **under-represent** music that fits the vibe but uses a different tag.
