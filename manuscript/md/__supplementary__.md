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

# Overview

%--
toc:
 exclude: [Overview]
--%

# Materials

Analysis scripts, data, stimuli (where possible given license restrictions), saliency maps, and luminance maps are available from <http://to.do/>.

# Linear mixed-effects models

The procedure used to construct the linear mixed-effects models (LME) is described in the main text. Models were estimated using the `lmer()` function from the `lme4` [v1.0, @Bates2014] package for R (v3.0.2).

%--
table:
 id: TblExp1
 source: exp1.csv
 caption:
  The LME for Exp. 1 used to estimate the partial slope of the relationship between pupil size and fixation saliency. Based on an LME model with by-participant random intercept and random slope for pupil size.
--%

%--
table:
 id: TblExp2
 source: exp2.csv
 caption:
  The LME for Exp. 2 used to estimate the partial slope of the relationship between pupil size and fixation saliency. Based on an LME model with by-participant random intercept and random slope for pupil size.
--%

%--
table:
 id: TblExp2Int
 source: exp2.int.csv
 caption:
  The LME for Exp. 2, including effects of stimulus type, task instruction, and relevant interaction terms. Fractals are used as reference stimulus type. Free-viewing is used as reference task instruction. Based on an LME model with by-participant random intercept and random slopes for pupil size, instruction, and stimulus type.
--%

%--
table:
 id: TblExp3Int
 source: exp3.int.csv
 caption:
  The LME for Exp. 3, including the effects of condition and condition x pupil size interaction. Dual task is used as reference condition. Based on an LME model with by-participant random intercept and random slopes for pupil size and condition.
--%

# Pupil-size transformations

%TblTransform lists the log-likelihood values of the LME models for different pupil-size transformations. High (i.e. less negative) log-likelihood values are better. The model shown in %TblExp1 corresponds to the *D*^-1^ model. Strikingly, transformations that reduce positive skewness work better than transformations that introduce positive skewness. Pupil-size area (*D*^2^), which we and others have frequently used as dependent measure [@Mathôt2013Plos;@Mathôt2014JVis;@Mathôt2014JExpPsy], is clearly suboptimal, at least for the present purpose.

%--
table:
 id: TblTransform
 source: transform.csv
 caption: |
  Log-likelihood values of LME models with different pupil-size transformations.
--%

# Relationship between luminance and saliency

It is well known that luminance is the primary determinant of pupil size [e.g., @Ellis1981]: The pupil constricts when looking at, or even attending to [@Binda2013Neurosci;@Mathôt2013Plos], bright surfaces. Therefore, if luminance were consistently and positively correlated with visual saliency, and if this were not controlled for, a pupillary light response might fully explain our results. Our primary way to control for this potential confound is by estimating pupillary luminance maps, and entering values from these maps as control predictor into the models, as described above and in the main text.

%--
figure:
 id: FigLumSal
 source: FigLumSal.svg
 caption: |
  The correlation between visual saliency and luminance. Dots correspond to individual images. a) The 200 images used for Exp. 1 and 3. b) The 50 natural scenes used for Exp. 2. c) The 50 3D fractals used for Exp. 2.
--%

However, it is also informative to directly consider the relation between luminance and saliency, in order to dispel any lingering suspicion that this may have confounded our results. As can be seen in %FigLumSal (see also the factor 'Fixation luminance' in Tables 1-3), the direction of this correlation varies widely from image to image, and also between the different image sets. (The values on the x-axis indicate the correlation coefficient between saliency and luminance values for the same pixel, separately for each image.) For the photos from the UPenn natural image database [@Tkačik2011], there was a weak negative correlation (a two-sided one-sample t-test against 0 on the correlation coefficients for each image: M = -.059, SE = .023, t(199) = 2.580, p = .011). This may reflect the fact that the primary source of brightness in the savanna is the sky, which is not very salient. For the images from the Campus Scene collection [@BurgeGeisler2011], there was a moderate positive correlation (M = .338, SE = 0.032, t(49) = 10.420, p < .001). This presumably reflects the fact that these images were taken in an urbanized environment, where bright lights are a dominant source of saliency. For the 3D Mandelbulber-generated fractals [@Marczak2012], there was also a moderate positive correlation (M = 0.272, SE = 0.043, t(49) = 6.259, p < 0.001), presumably due to the use of virtual light sources.

For our purpose, the crucial point to note is that the correlation between saliency and brightness is variable, and can be positive or negative depending on the specifics of the stimuli. However, the correlation between pupil size and saliency is invariably negative (or positive when using an inverse transformation), and can therefore not be (fully) related to brightness.

# Acknowledgements

%-- include: md/acknowledgements.md --%
