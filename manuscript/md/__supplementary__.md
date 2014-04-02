---
title:
 "Large Pupils Predict Goal-driven Eye Movements (supplementary material)"
author:
  Sebastiaan Mathôt^1^, Alisha Siebold^2^, Mieke Donk^2^, and Françoise Vitu^1^
affiliation:
 - ^1^ Aix-Marseille University, CNRS, LPC UMR 7290, Marseille, France
 - ^2^ Dept. of Cognitive Psychology, VU University Amsterdam
correspondence:
 - Aix-Marseille University, CNRS
 - Laboratoire de Psychologie Cognitive, UMR 7290
 - 3 Place Victor Hugo
 - Centre St. Charles, Bâtiment 9, Case D
 - 13331 Marseille
 - France
---

# Materials

Analysis scripts, data, stimuli (where possible given license restrictions), saliency maps, and luminance maps are available from <http://to.do/>.

# Linear mixed-effects models

The procedure used to construct the linear mixed-effects models (LMM) is described in the main text. Because model slopes depend on the range of values that the predictor can take (i.e. a wide range leads to a shallow slope), we calculated the 'Absolute Normalized Slope' (ANS) as `|Slope x Std|`. Here, `Slope` corresponds to the LMM slopes listed in the tables below and `Std` corresponds to the standard deviation of the predictor across the full dataset. The ANS provides a rough indication of the effect size of the predictors, in the sense that the various slopes are cast into comparable normalized units. (But not in the sense that they directly reflect the reliability of the effect.)

Across the three experiments, pupil size is one of the strongest predictors of fixation saliency, with only vertical fixation position being systematically more predictive (see %TblExp1Partial, %TblExp2Partial, and %TblExp3SinglePartial). (No full-LME model is shown for the dual-task condition of Exp. 3, because pupil size was not included in the preferred model.) The direct relationship (i.e. from a model with only pupil size as fixed effect) between pupil size and fixation saliency is shown for all experiments in %TblDirect. The direct relationships are comparable to the partial relationships, suggesting that the relationship between pupil size and fixation saliency is relatively independent of the other factors that were considered.

Models were estimated using the `lmer()` function from the `lme4` [v0.999999-2, @Bates2014] package for R (v3.0.1).

%--
table:
 id: TblExp1Partial
 source: exp1.partial.csv
 caption:
  The full LME for Exp. 1, used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblExp2Partial
 source: exp2.partial.csv
 caption:
  The full LME for Exp. 2, used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblExp3SinglePartial
 source: exp3.partial.single.csv
 caption: 
  The full LME for the single-task condition of Exp. 3, used to estimate the partial slope of the relationship between pupil size and fixation saliency.
--%

%--
table:
 id: TblDirect
 source: direct.lme.csv
 caption: |
  The direct slope of the relationship between pupil size and fixation saliency for Exp. 1, Exp. 2, Exp. 3 (single task), and Exp 3. (dual task). These slopes were estimated using a model with only pupil size as fixed effect.
--%

# Relationship between luminance and saliency

It is well known that luminance is the primary determinant of pupil size [e.g., @Ellis1981]: The pupil constricts when looking at, or even attending to [@Binda2013Neurosci;@Mathôt2013Plos], bright surfaces. Therefore, if luminance were consistently and positively correlated with visual saliency, and if this were not controlled for, a pupillary light response might fully explain our results. Our primary way to control for this potential confound is by estimating pupillary luminance maps, and entering values from these maps as fixed effects into the models, as described above and in the main text.

%--
figure:
 id: FigLumSal
 source: luminance-saliency.svg
 caption: |
  The correlation between visual saliency and luminance. Dots correspond to individual images. a) The 200 images used for Exp. 1 and 3. b) The 50 natural scenes used for Exp. 2. c) The 50 3D fractals used for Exp. 2.
--%

However, it is also informative to directly consider the relation between luminance and saliency, in order to dispel any lingering suspicion that this may have confounded our results. As can be seen in %FigLumSal (see also the factor 'Fixation luminance' in Tables 1-3), the direction of this correlation varies widely from image to image, and also between the different image sets. (The values on the x-axis indicate the correlation coefficient between saliency and luminance values for the same pixel, separately for each image.) For the photos from the UPenn natural image database [@Tkačik2011], there was a weak negative correlation (a two-sided one-sample t-test against 0 on the correlation coefficients for each image: M = -.059, SE = .023, t(199) = 2.580, p = .011). This may reflect the fact that the primary source of brightness in the savanna is the sky, which is not very salient. For the images from the Campus Scene collection [@BurgeGeisler2011], there was a moderate positive correlation (M = .338, SE = 0.032, t(49) = 10.420, p < .001). This presumably reflects the fact that these images were taken in an urbanized environment, where bright lights are a dominant source of saliency. For the 3D Mandelbulber-generated fractals [@Marczak2012], there was also a moderate positive correlation (M = 0.272, SE = 0.043, t(49) = 6.259, p < 0.001), presumably due to the use of virtual light sources.

For our purpose, the crucial point to note is that the correlation between saliency and brightness is variable, and can be positive or negative depending on the specifics of the stimuli. However, the correlation between pupil size and saliency is invariably negative, and can therefore not be (fully) related to brightness.

# Interactive analysis (Exp. 3)

To avoid unmanageable complexity, and to reduce "researcher's degrees of freedom" [@Simmons2011Flexibility], we have used the same additive-model building algorithm for all main analyses (presented in the main text). However, there are multiple ways to analyze datasets such as the present, and we also conducted an exploratory interactive analysis for Exp. 3, to further test how the relationship between pupil size and fixation saliency is modulated by condition (single vs dual task).

First, using the same method as before, we constructed an additive model using the full dataset from Exp. 3. Next, we added the pupil-size-by-condition interaction term to the model (%TblExp3IntPartial). Like before, we also created a minimal LME (for the direct relationship), which included only pupil size and the pupil-size-by-condition interaction as fixed effects (%TblExp3IntDirect). 

%--
table:
 id: TblExp3IntPartial
 source: interaction.partial.csv
 caption: |
  The full LME for Exp. 3, including the pupil-size by condition interaction term.
--%

%--
table:
 id: TblExp3IntDirect
 source: interaction.direct.csv
 caption: |
  The minimal LME for Exp. 3, including the pupil-size by condition interaction term.
--%

The difference between the partial (%TblExp3IntPartial) and direct (%TblExp3IntDirect) pupil-size-by-condition interaction is substantial. This suggests that some of the other predictors in the LME are also affected by condition, and also correlate with fixation saliency and pupil size. In an attempt to understand these correlations, we iteratively removed one predictor from the full LME, and, conversely, added it to the simplified LME. This revealed that the difference between the partial and direct interaction was largely due to two factors: trial number and fixation eccentricity. Below we provide a best guess of why this is, but we acknowledge that it is far from trivial to characterize these types of complex interactions.

Firstly, as can be seen in %TblExp3IntPartial, trial number is positively related to fixation saliency. This likely reflects a fatigue effect: As the experiment progresses, participants grow tired, invest less mental effort in the task, and consequently fixate more salient locations. Fatigue also leads to a constriction of the pupil [@Lowenstein1963Fatigue]. Importantly, it appears that fatigue increases more in the dual-task than in the single-task condition, and trial number therefore captures some of the variance of the pupil-size-by-condition interaction. In other words, the addition of a dual task reduced the amount of mental effort invested in the visual-search also by increasing overall fatigue, and not only by 'redirecting' mental effort towards the primary task.

Secondly, fixation eccentricity is negatively related to fixation saliency (%TblExp3IntPartial). This is because most photos are composed such that the more salient objects are in the center. Because of this composition bias, as well as other reasons [@Tatler2007], people look at the (salient) center of a photo more than at its edges. Consequently, there is a triadic relationship between fixation saliency, fixation eccentricity, and pupil size. Interestingly, the central fixation bias is larger in the dual-task than the single-task condition, reminiscent of the 'tunnel vision' that arises when drivers have a conversation on the phone [@NunesRecarte2002]. Therefore, fixation eccentricity captures some of the variance of the pupil-size-by-condition interaction. Although the central fixation bias is not our main focus, we note that the fact that it increases in the dual-task condition suggests that it is, at least in part, a default mode. Not unlike the tendency to fixate salient locations, the tendency to fixate the display center may be a default eye-movement behavior that participants fall back to when they do not invest much mental effort.
