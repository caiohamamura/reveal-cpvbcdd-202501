# Aula12: Cluster Analysis

# Clustering Lesson Plan: Brazilian Pants Sizes as a Real-World Example

## General Idea

Brazilian pants sizing is an excellent concrete example for clustering because:

- Sizes are discrete (36, 38, 40, ... 54)
- Human bodies are continuous and multidimensional
- Manufacturers compress many body shapes into a small number of categories
- Different body proportions exist:
  - tall and thin
  - short and wide
  - athletic
  - curvy
  - outliers
- The problem is intuitive and connected to students' daily lives

This creates a natural motivation for clustering:

> "How can a clothing company group similar body types into a limited number of standardized sizes?"

---

# Learning Objectives

By the end of the lesson students should be able to:

- Understand clustering as unsupervised learning
- Explain the difference between classification and clustering
- Interpret clusters visually
- Apply:
  - Hierarchical Clustering
  - K-Means
  - DBSCAN
- Understand strengths and weaknesses of each method
- Discuss how real-world constraints influence data modeling

---

# Suggested Structure

## Total Duration

Recommended: 4 hours

- 1h 15min theory and discussion
- 2h 15min hands-on notebook
- 30min discussion and interpretation

---

# Part 1 — Problem Introduction (15–20 min)

## Classroom Discussion

Start with questions:

- Why do clothing sizes exist?
- Why aren't all pants custom-made?
- Why can two people using size 42 have very different bodies?
- Why do some brands fit differently?
- Why do some people say:
  - "42 is too tight in the waist"
  - "44 is too long"
  - "Fits the hip but not the leg"

Then introduce:

> Manufacturers must compress continuous human variation into a small number of categories.

This is essentially a clustering problem.

---

# Part 2 — Building the Dataset

## Option A (Recommended): Synthetic Dataset

Synthetic data is actually ideal pedagogically because:

- You control the clusters
- You can create overlaps
- You can create outliers
- You can create density differences
- You can gradually increase complexity

---

# Variables to Use

Use only 2 variables initially.

## Recommended Variables

- Waist circumference (cm)
- Leg length / inseam (cm)

This creates the exact issue Brazilian sizing has:

Two people may have the same waist but very different leg lengths.

---

# Initial Dataset Design

Create 4 natural body groups:

| Group | Waist | Leg Length | Interpretation |
|---|---|---|---|
| A | Small | Short | Short/thin |
| B | Small | Long | Tall/thin |
| C | Large | Short | Short/wide |
| D | Large | Long | Tall/wide |

Each group can contain ~50 samples.

Add:

- random noise
- overlapping boundaries
- a few outliers

Total:

- 200–250 points

---

# Visual Intuition

Students should immediately see:

- natural groups
- overlaps
- imperfect boundaries
- outliers

This is important because clustering becomes visually intuitive.

---

# First Plot (VERY IMPORTANT)

## Scatter Plot

X-axis:
- Waist circumference

Y-axis:
- Leg length

Discuss:

- Do you visually see groups?
- How many?
- Are boundaries obvious?
- Are there ambiguous people?
- Could one size satisfy all?

This discussion is essential before introducing algorithms.

---

# Suggested Synthetic Data Parameters

## Group A — Short/Thin

- Waist: mean 72 cm
- Leg: mean 72 cm

## Group B — Tall/Thin

- Waist: mean 74 cm
- Leg: mean 92 cm

## Group C — Short/Wide

- Waist: mean 98 cm
- Leg: mean 74 cm

## Group D — Tall/Wide

- Waist: mean 102 cm
- Leg: mean 94 cm

Use normal distributions with moderate variance.

Example:

- std waist = 5
- std leg = 4

---

# Optional Real Datasets

## 1. CAESAR Anthropometric Dataset

The best real-world candidate.

Contains:

- body measurements
- waist
- hip
- inseam
- height
- weight

Widely used in ergonomic and apparel studies.

Challenges:

- harder to access
- licensing restrictions in some cases
- very large

Useful more as inspiration than for classroom simplicity.

---

## 2. Kaggle Body Measurement Datasets

Possible search terms:

- "body measurements"
- "anthropometric dataset"
- "fashion sizing"

Some datasets include:

- height
- waist
- chest
- hip
- BMI

These are useful for advanced exercises.

---

# Part 3 — Hierarchical Clustering

## Pedagogical Goal

Introduce clustering visually and conceptually.

Hierarchical clustering is excellent because:

- no need to initially specify k visually
- students can literally see clusters forming
- dendrograms are intuitive

---

# Teaching Sequence

## Step 1 — Distance Concept

Discuss:

- What makes two people "similar"?
- Euclidean distance
- Similarity in feature space

Plot two points and draw the distance.

---

# Step 2 — Agglomerative Idea

Explain:

1. Every point starts alone
2. Closest points merge
3. Clusters merge progressively
4. Eventually everything becomes one cluster

Use animation if possible.

---

# Important Plot

## Dendrogram

Students should learn:

- vertical height = distance of merge
- big jumps indicate natural separations

Discussion:

- Where should we cut?
- How many clusters seem reasonable?

---

# Then Plot Colored Clusters

Show:

- scatter plot with cluster colors

Discuss:

- Are groups meaningful?
- Did the algorithm separate tall-thin from short-thin?
- What happens in overlapping regions?

---

# Key Discussion Points

## Advantages

- interpretable
- visual
- no initial k required conceptually
- good for exploration

## Weaknesses

- computationally expensive
- sensitive to linkage choice
- difficult for very large datasets

---

# Part 4 — K-Means

## Pedagogical Goal

Introduce centroid-based clustering.

This is probably the easiest algorithm mathematically.

---

# Start With the Real-World Interpretation

Explain:

A company may decide:

> "We will create 4 representative body types."

Each centroid becomes a representative size pattern.

This is a fantastic intuitive analogy.

---

# Teaching Sequence

## Step 1 — Initial Centroids

Randomly place centroids.

Show:

- centroids on scatter plot

---

## Step 2 — Assignment

Each person belongs to nearest centroid.

Color regions.

---

## Step 3 — Recompute Mean

Move centroid to average position.

Repeat.

---

# Important Visuals

## Animation

Students LOVE seeing centroids move.

This is one of the best visual ML demonstrations.

---

# Elbow Method

## Excellent Discussion Opportunity

Question:

> How many sizes should the manufacturer create?

This maps perfectly to choosing k.

Plot:

- x-axis = k
- y-axis = inertia / SSE

Discuss:

- diminishing returns
- business tradeoffs
- too many sizes vs too few

---

# Important Conceptual Discussion

## Compression of Reality

K-means literally compresses continuous variability into prototypes.

This is exactly what clothing sizes do.

That analogy is extremely powerful.

---

# Key Discussion Points

## Advantages

- fast
- scalable
- intuitive
- easy to implement

## Weaknesses

- must choose k
- assumes spherical clusters
- sensitive to initialization
- struggles with irregular shapes

---

# Excellent Transition to DBSCAN

Now intentionally create a dataset where:

- clusters are not spherical
- densities vary
- outliers exist

Then show K-means failing.

This creates the motivation for DBSCAN naturally.

---

# Part 5 — DBSCAN

## Important Pedagogical Advice

Do NOT use the pants dataset first.

DBSCAN shines in:

- arbitrary shapes
- density-based groups
- noisy data

The pants example is actually fairly friendly to K-means.

That is GOOD pedagogically.

Students first learn where K-means works.

Then they learn where it fails.

---

# Recommended DBSCAN Dataset

## Option 1 — Shopping Mall Corridors

Generate:

- curved clusters
- elongated shapes
- noise

Interpretation:

People move in patterns.

---

## Option 2 — City Neighborhoods

Generate:

- dense urban centers
- sparse suburbs
- isolated houses

Interpretation:

Density matters.

---

## Option 3 (BEST) — Human Body Shapes with Rare Groups

Extend the clothing example.

Create:

- normal groups
- a small athletic group
- rare body proportions
- extreme outliers

Show:

K-means forces everyone into clusters.

DBSCAN can:

- isolate noise
- detect dense groups
- ignore outliers

This keeps narrative continuity.

---

# Teaching Sequence for DBSCAN

## Core Concepts

Introduce:

- epsilon neighborhood
- minimum points
- core points
- border points
- noise points

---

# Essential Visualization

For a selected point draw:

- epsilon radius circle
- neighboring points

This helps students understand density.

---

# Then Show Final Clusters

Highlight:

- arbitrary shapes
- noise points labeled separately

---

# Important Discussion

## Why DBSCAN is Different

K-means asks:

> Which centroid is closest?

DBSCAN asks:

> Is this region dense enough?

That conceptual contrast is very important.

---

# Final Comparative Discussion

# Comparative Table

| Method | Main Idea | Needs k? | Handles Noise? | Handles Arbitrary Shapes? |
|---|---|---|---|---|
| Hierarchical | Progressive merging | Optional | Poorly | Sometimes |
| K-Means | Centroids | Yes | No | No |
| DBSCAN | Density | No | Yes | Yes |

---

# Excellent Classroom Questions

## Business Questions

- Should a company create more sizes?
- What is the cost of too many sizes?
- What happens to people far from centroids?
- Are minority body types excluded?
- How does data influence inclusion?

This creates a fantastic interdisciplinary discussion.

---

# Suggested Notebook Flow

# Section 1 — Generate Synthetic Data

Students:

- generate groups
- visualize data
- inspect overlaps

---

# Section 2 — Hierarchical Clustering

Students:

- compute linkage
- plot dendrogram
- cut tree
- visualize clusters

---

# Section 3 — K-Means

Students:

- run K-means
- visualize centroids
- compute elbow method
- compare different k

---

# Section 4 — DBSCAN

Students:

- generate non-spherical data
- vary epsilon
- vary min_samples
- observe noise handling

---

# Section 5 — Comparison

Students discuss:

- which method fits which scenario
- computational tradeoffs
- interpretability
- robustness

---

# Very Important Conceptual Point

## Clustering Has No Absolute Truth

This lesson is excellent for teaching:

> Clusters are often modeling choices, not objective truths.

Two companies may define sizes differently.

Different algorithms may produce different groups.

This is a profound and important data science lesson.

---

# Optional Advanced Extensions

## Add More Dimensions

After 2D:

Add:

- hip circumference
- thigh circumference
- height
- weight

Then discuss:

- curse of dimensionality
- visualization challenges
- PCA later in course

---

# Optional Ethical Discussion

## Bias and Representation

Questions:

- What body types become underrepresented?
- What happens when data is collected mostly from one population?
- How can clustering reinforce exclusion?

Very relevant socially and industrially.

---

# Recommended Python Libraries

- numpy
- pandas
- matplotlib
- seaborn (optional)
- scipy
- scikit-learn

---

# Suggested Deliverable

Students could write:

1. Which clustering method worked best?
2. What assumptions does each method make?
3. What would they recommend for a clothing company?
4. What limitations exist in standardized sizing?

---

# Suggested Synthetic Dataset Generator (Conceptual)

You can generate data from Gaussian distributions:

- cluster 1 = normal(72, 5)
- cluster 2 = normal(74, 5)
- etc.

Then concatenate all groups into a dataframe.

---

# Final Pedagogical Advantage of This Example

This example is strong because:

- intuitive
- visual
- relatable
- socially relevant
- naturally multidimensional
- naturally imperfect
- creates ambiguity
- connects ML to industrial decisions

It is much stronger pedagogically than abstract geometric toy examples alone.

