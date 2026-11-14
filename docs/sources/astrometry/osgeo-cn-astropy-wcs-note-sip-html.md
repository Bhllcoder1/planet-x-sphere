---
source: https://osgeo.cn/astropy/wcs/note_sip.html
fetched: 2026-11-14
status: 200
---

关于SIP和WCS的说明 — Astropy v7.1.0

[跳转至主要内容](#main-content)

回到顶部


`Ctrl`+`K`

[![Astropy v7.1.0 - Home](../_static/astropy_banner_96.png)![Astropy v7.1.0 - Home](../_static/astropy_banner_96_dark.png)](../index.html)

* [开始](../index_getting_started.html)
* [用户指南](../index_user_docs.html)
* [贡献](../index_dev.html)
* [项目详情](../index_project_details.html)
* [Tutorials](https://learn.astropy.org/)

搜索
`Ctrl`+`K`

* [GitHub](https://github.com/astropy/astropy "GitHub")

搜索
`Ctrl`+`K`

* [开始](../index_getting_started.html)
* [用户指南](../index_user_docs.html)
* [贡献](../index_dev.html)
* [项目详情](../index_project_details.html)
* [Tutorials](https://learn.astropy.org/)

* [GitHub](https://github.com/astropy/astropy "GitHub")

* 关于SIP和WCS的说明

关于SIP和WCS的说明[#](#note-about-sip-and-wcs "Link to this heading")
===============================================================

[`astropy.wcs`](reference_api.html#module-astropy.wcs "astropy.wcs") supports the Simple Imaging Polynomial ([SIP](https://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/shupeADASS.pdf)) 惯例。SIP失真通过SIP特定关键字的存在在FITS头中定义 **and** 一 `-SIP` 后缀in `CTYPE` ，例如 `RA---TAN-SIP` ， `DEC--TAN-SIP` .

这在过去并不是一个严格的惯例 [`astropy.wcs`](reference_api.html#module-astropy.wcs "astropy.wcs") 如果存在SIP系数，则始终包括SIP失真，即使 `-SIP` 不包括在CTYPE中。一个 `-SIP` CTYPE中的后缀不用作初始化SIP失真的触发器。

报头正确实现SIP约定是很重要的。如果目的是使用SIP失真，则报头应该具有SIP系数和 `-SIP` CTYPE中的后缀。

[`astropy.wcs`](reference_api.html#module-astropy.wcs "astropy.wcs") 当检测到不一致的报头时，例如当存在SIP系数但CTYPE缺少a时，打印INFO消息 `-SIP` 后缀，见下面的例子。 [`astropy.wcs`](reference_api.html#module-astropy.wcs "astropy.wcs") 将打印有关不一致标头的消息，但将创建和使用SIP失真，并将在调用中使用 [`all_pix2world`](../api/astropy.wcs.WCS.html#astropy.wcs.WCS.all_pix2world "astropy.wcs.wcs.WCS") . 如果这不是预期用途（例如，这是一个毛毛雨的图像，没有失真），最好从头部删除SIP系数。可以通过以下方法从WCS对象中临时删除它们

```
>>> wcsobj.sip = None

```

另外，如果SIP是报头中唯一的失真，那么这两种方法， [`wcs_pix2world`](../api/astropy.wcs.WCS.html#astropy.wcs.WCS.wcs_pix2world "astropy.wcs.wcs.WCS") 和 [`wcs_world2pix`](../api/astropy.wcs.WCS.html#astropy.wcs.WCS.wcs_world2pix "astropy.wcs.wcs.WCS") ，可用于从像素到世界坐标系的转换，同时忽略失真。

头不一致的另一个后果是如果 [`to_header()`](../api/astropy.wcs.WCS.html#astropy.wcs.WCS.to_header "astropy.wcs.wcs.WCS") 被调用 `relax=True` 它将返回一个带有SIP系数和 `-SIP` 后缀在CTYPE中，不会复制原始标头。

**总之，什么时候 ``astropy.wcs`` 检测不一致的标头，建议检查并更正标头以匹配数据。**

下面是具有SIP系数的报头的示例，当 `-SIP` CTYPE中缺少。数据是毛毛雨，即无失真，因此目的是 **not** 包括SIP失真。

```
>>> wcsobj = wcs.WCS(header)
INFO:

        Inconsistent SIP distortion information is present in the FITS header and the WCS object:
        SIP coefficients were detected, but CTYPE is missing a "-SIP" suffix.
        astropy.wcs is using the SIP distortion coefficients,
        therefore the coordinates calculated here might be incorrect.

        If you do not want to apply the SIP distortion coefficients,
        please remove the SIP coefficients from the FITS header or the
        WCS object.  As an example, if the image is already distortion-corrected
        (e.g., drizzled) then distortion components should not apply and the SIP
        coefficients should be removed.

        While the SIP distortion coefficients are being applied here, if that was indeed the intent,
        for consistency please append "-SIP" to the CTYPE in the FITS header or the WCS object.

```

```
>>> hdr = wcsobj.to_header(relax=True)
INFO:

        Inconsistent SIP distortion information is present in the current WCS:
        SIP coefficients were detected, but CTYPE is missing "-SIP" suffix,
        therefore the current WCS is internally inconsistent.

        Because relax has been set to True, the resulting output WCS will have
        "-SIP" appended to CTYPE in order to make the header internally consistent.

        However, this may produce incorrect astrometry in the output WCS, if
        in fact the current WCS is already distortion-corrected.

        Therefore, if current WCS is already distortion-corrected (eg, drizzled)
        then SIP distortion components should not apply. In that case, for a WCS
        that is already distortion-corrected, please remove the SIP coefficients
        from the header.

```

[编辑](https://github.com/astropy/astropy/edit/main/docs/wcs/note_sip.rst)

© Copyright 2011–2025, The Astropy Developers.

由 [Sphinx](https://www.sphinx-doc.org/) 8.2.3创建。

使用 [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.16.1构建.

## Links found on page

- https://github.com/astropy/astropy
- https://github.com/astropy/astropy/edit/main/docs/wcs/note_sip.rst
- https://irsa.ipac.caltech.edu/data/SPITZER/docs/files/spitzer/shupeADASS.pdf
- https://learn.astropy.org/
- https://osgeo.cn/astropy/api/astropy.wcs.WCS.html#astropy.wcs.WCS.all_pix2world
- https://osgeo.cn/astropy/api/astropy.wcs.WCS.html#astropy.wcs.WCS.to_header
- https://osgeo.cn/astropy/api/astropy.wcs.WCS.html#astropy.wcs.WCS.wcs_pix2world
- https://osgeo.cn/astropy/api/astropy.wcs.WCS.html#astropy.wcs.WCS.wcs_world2pix
- https://osgeo.cn/astropy/index.html
- https://osgeo.cn/astropy/index_dev.html
- https://osgeo.cn/astropy/index_getting_started.html
- https://osgeo.cn/astropy/index_project_details.html
- https://osgeo.cn/astropy/index_user_docs.html
- https://osgeo.cn/astropy/wcs/reference_api.html#module-astropy.wcs
- https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
- https://www.sphinx-doc.org/
